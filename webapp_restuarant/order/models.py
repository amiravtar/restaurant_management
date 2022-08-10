from django.db import models
from django.db.models.signals import pre_delete, m2m_changed
from django.dispatch import receiver
from utils.date_persian import date_fromgregorian
from django.core.exceptions import ValidationError

from deliver.models import Deliver
import logging

# Create your models here.

logger = logging.getLogger("app")


class FoodCount(models.Model):
    food = models.ForeignKey("food.Food", on_delete=models.CASCADE)
    count = models.IntegerField()

    def __str__(self):
        return "|".join([self.food.name, str(self.count)])

    @property
    def total_price(self):
        return self.food.price * self.count


class FixMenu(models.Model):
    class Meta:
        verbose_name = "منوی ثابت"
        verbose_name_plural = "منو های ثابت"

    name = models.CharField("نام منو", max_length=50)
    restaurant = models.ForeignKey(
        "restaurant.Restaurant", verbose_name="رستوران", on_delete=models.CASCADE
    )
    foods = models.ManyToManyField("food.Food", verbose_name="غذا ها")

    def __str__(self):
        return " | ".join([self.name, str([f.name for f in self.foods.all()])])


class DateFoodCount(models.Model):
    """_summary_

    Store Food and count of it for a spesific date.
    whene somebody order that food count gana reduce by order count
    """

    food = models.ForeignKey("food.Food", on_delete=models.CASCADE)
    count = models.IntegerField()

    def __str__(self):
        return " | ".join([self.food.name, str(self.count)])
        # return " | ".join(
        #     [
        #         self.food.name,
        #         str(self.count),
        #         str(self.order_date.count()),
        #         str(self.order_date.get().id if self.order_date.exists() else "N"),
        #     ]
        # )


class OrderDate(models.Model):
    """_summary_

    Spesify a date.
    store some count of foods.

    """

    class Meta:
        verbose_name = "منوی تاریخ دار"
        verbose_name_plural = "منو های تاریخ دار"

    date = models.DateField(
        auto_now=False, auto_now_add=False, unique=True, verbose_name="تاریخ"
    )
    foods = models.ManyToManyField(
        DateFoodCount, blank=True, related_name="order_date", verbose_name="غذاها"
    )
    restaurant = models.ForeignKey(
        "restaurant.Restaurant", on_delete=models.CASCADE, verbose_name="رستوران مربوطه"
    )
    fix_menu = models.ForeignKey(
        FixMenu,
        verbose_name="منوی ثابت",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    disable = models.BooleanField(verbose_name="غیر فعال", default=False)

    def __str__(self):
        return date_fromgregorian(self.date).strftime("%Y/%m/%d %b %a")
        # return (
        #     date_fromgregorian(self.date).strftime("%Y/%m/%d %b %a")
        #     + "|"
        #     + str(self.id)
        # )


@receiver(pre_delete, sender=OrderDate)
def order_date_pre_delete(sender, instance, **kwargs):
    for i in instance.foods.all():
        i.delete()


@receiver(m2m_changed, sender=OrderDate.foods.through)
def order_date_post_save(sender, instance, action, **kwargs):
    if action == "post_add":
        for i in instance.foods.all():
            if instance.fix_menu:
                if i in instance.fix_menu:
                    instance.foods.remove(i)
                    continue
            if i.order_date.count() > 1:
                dfc = DateFoodCount(food=i.food, count=i.count)
                dfc.save()
                instance.foods.remove(i)
                instance.foods.add(dfc)


class Order(models.Model):
    TAKEOUT = "takeout"
    DELIVER = "deliver"
    RECEIVE_TYPE = [
        (TAKEOUT, "تحویل حضوری"),
        (DELIVER, "ارسال درب منزل"),
    ]

    TEMP = "temp"
    PENDING_CONFIRM = "pending_confirm"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    DELIVERY = "delivery"
    DELIVERED = "delivered"
    FAILED = "failed"
    NOT_CONFIRM = "not_confirmed"

    ORDER_STATUS = [
        (TEMP, "موقت"),
        (PENDING_CONFIRM, "در انتظار تایید"),
        (CONFIRMED, "سفارش پذیرفته شده"),
        (IN_PROGRESS, "در حال آماده سازی"),
        (DELIVERY, "تحویل به پیک"),
        (DELIVERED, "تحویل داده شده به مشتری"),
        (FAILED, "به مشکل برخورده"),
        (NOT_CONFIRM, "تایید نشده"),
    ]

    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, verbose_name="کاربر"
    )
    restaurant = models.ForeignKey(
        "restaurant.Restaurant",
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="رستوران  ",
    )
    receive_type = models.CharField(
        max_length=20, blank=True, null=True, choices=RECEIVE_TYPE
    )
    status = models.CharField(
        choices=ORDER_STATUS, max_length=50, default=TEMP, verbose_name="وضعیت"
    )

    description = models.TextField(null=True, blank=True, verbose_name="توضیحات")
    foods = models.ManyToManyField(FoodCount, blank=True, verbose_name="غذاها")
    created_on = models.DateTimeField(auto_now_add=True)
    address = models.CharField(
        max_length=70, null=True, blank=True, verbose_name="آدرس گیرنده"
    )
    target_date = models.DateField(
        auto_now=False, auto_now_add=False, verbose_name="تاریخ تحویل سفارش"
    )
    order_date = models.ForeignKey(
        OrderDate,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="تاریخ مرجع",
    )

    # Managers
    def __str__(self):
        return " | ".join([self.restaurant.name, self.user.full_name, self.status])

    def get_order_date(self):
        date = OrderDate.objects.filter(
            date=self.target_date, restaurant=self.restaurant
        )
        if date.exists():
            self.order_date = date[0]
            self.save()
            return self
        else:
            return None

    @property
    def sum_foods_price(self):
        "Return sum of foods price base count except cost of delivery"
        return sum(food.total_price for food in self.foods.all())

    @property
    def total_foods_price(self):
        sumf = self.sum_foods_price
        return sumf + int(sumf * self.restaurant.tax_food / 100)

    @property
    def food_tax(self):
        sumf = self.sum_foods_price
        return int(sumf * self.restaurant.tax_food / 100)

    @property
    def food_counts(self):
        "return counts of food's order"
        return sum(item.count for item in self.foods.all())

    # calculate total orders price no tax
    @property
    def total_price(self):
        return int(
            self.total_delivery_fee + self.total_foods_price + self.restaurant.tax_fix
        )

    @property
    def get_delivery_fee(self):
        delivery = 0
        if self.receive_type == self.DELIVER:
            delivery = self.restaurant.deliver_fee
        return delivery

    @property
    def total_delivery_fee(self):
        fee = self.get_delivery_fee
        return fee + int(fee * self.restaurant.tax_delivery / 100)

    @property
    def delivery_tax(self):
        fee = self.get_delivery_fee
        return int(fee * self.restaurant.tax_delivery / 100)

    @property
    def fix_tax(self):
        return self.restaurant.tax_fix

    def show_receive_type(self):
        status_dict = dict(self.RECEIVE_TYPE)
        return status_dict[self.receive_type]

    def show_status_name(self):
        status_choices_dict = dict(self.ORDER_STATUS)
        return status_choices_dict[self.status]

    @property
    def show_deliver_status_name(self):
        status_choices_dict = dict(Deliver.STATUS_TYPE)
        return status_choices_dict[self.deliver.get().status]

    @property
    def get_created_date(self):
        return date_fromgregorian(self.created_on).strftime("%Y/%m/%d %H:%M")

    @property
    def get_target_date(self):
        return date_fromgregorian(self.target_date).strftime("%Y/%m/%d")

    @property
    def is_deletable(self):
        return self.status in [self.TEMP, self.PENDING_CONFIRM]

    @property
    def is_delivery(self):
        return self.deliver.exists()

    @property
    def is_takeout(self):
        return self.receive_type == self.TAKEOUT

    @property
    def get_deliver_drive_name(self):
        try:
            return self.deliver.get().driver.full_name
        except Exception as e:
            logger.error(e)
            return ""

    @property
    def get_deliver_drive_phone(self):
        try:
            return self.deliver.get().driver.user.profile.phone
        except Exception as e:
            logger.error(e)
            return ""


@receiver(pre_delete, sender=Order)
def order_pre_delete(sender, instance, **kwargs):
    if instance.order_date == None:
        raise ValidationError("سفارش انتخابی تاریخ مرجعی ندارد")
    order_date = instance.order_date
    dfcs = DateFoodCount.objects.filter(order_date__id=order_date.id)
    for fc in instance.foods.all():
        df = dfcs.filter(food=fc.food)
        if df.exists():
            df = df[0]
        else:
            if order_date.fix_menu and order_date.fix_menu.foods.contains(fc.food):
                continue
            else:
                logger.error(
                    "DateFoodCount with food {0} Dosent exist for this order {1}".format(
                        fc.food, instance.id
                    )
                )
            raise ValidationError("غذای مورد نظر پیدا نشد")
        df.count = df.count + fc.count
        df.save()
