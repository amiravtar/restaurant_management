from django.db import models
from django.db.models.signals import pre_delete, m2m_changed
from django.dispatch import receiver
from utils.date_persian import date_fromgregorian
from django.core.exceptions import ValidationError
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


class DateFoodCount(models.Model):
    """_summary_

    Store Food and count of it for a spesific date.
    whene somebody order that food count gana reduce by order count
    """

    food = models.ForeignKey("food.Food", on_delete=models.CASCADE)
    count = models.IntegerField()

    def __str__(self):
        return " | ".join([self.food.name, str(self.count)])


class OrderDate(models.Model):
    """_summary_

    Spesify a date.
    store some count of foods.

    """

    date = models.DateField(
        auto_now=False, auto_now_add=False, unique=True, verbose_name="تاریخ"
    )
    foods = models.ManyToManyField(
        DateFoodCount, blank=True, related_name="order_date", verbose_name="غذاها"
    )
    restaurant = models.ForeignKey(
        "restaurant.Restaurant", on_delete=models.CASCADE, verbose_name="رستوران مربوطه"
    )

    def __str__(self):
        return date_fromgregorian(self.date).strftime("%Y/%m/%d %b %a")


@receiver(pre_delete, sender=OrderDate)
def order_date_pre_delete(sender, instance, **kwargs):
    for i in instance.foods.all():
        i.delete()


@receiver(m2m_changed, sender=OrderDate.foods.through)
def order_date_post_save(sender, instance, action, **kwargs):
    if action == "post_add":
        for i in instance.foods.all():
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
    def food_counts(self):
        "return counts of food's order"
        return sum(item.count for item in self.foods.all())

    # calculate total orders price no tax
    @property
    def total_price(self):
        return self.get_delivery_fee + self.sum_foods_price
        # TODO:Add tax

    @property
    def get_delivery_fee(self):
        delivery = 0
        if self.receive_type == self.DELIVER:
            delivery = self.restaurant.deliver_fee
        return delivery
        # TODO:Add tax

    def show_receive_type(self):
        status_dict = dict(self.RECEIVE_TYPE)
        return status_dict[self.receive_type]

    def show_status_name(self):
        status_choices_dict = dict(self.ORDER_STATUS)
        return status_choices_dict[self.status]

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
        return self.receive_type ==Order.DELIVER
    

