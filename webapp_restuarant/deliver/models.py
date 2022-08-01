from datetime import datetime
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from order.models import Order
from django.core.exceptions import ValidationError

# Create your models here.
class Deliver(models.Model):
    INWAY = "inway"
    WAIT_FOR_READY = "wating_for_ready"
    PICKUP = "pickup"
    DELIVERD = "deliverd"
    NDELIVERD = "ndeliverd"
    STATUS_TYPE = [
        (INWAY, "در راه"),
        (PICKUP, "در حال دریافت از رستوران"),
        (DELIVERD, "تحویل داده شده"),
        (NDELIVERD, "تحویل داده نشده"),
        (WAIT_FOR_READY, "در انتظار آماده سازی"),
    ]
    driver = models.ForeignKey("restaurant.driver", on_delete=models.CASCADE)
    order = models.ForeignKey(
        "order.Order", on_delete=models.CASCADE, related_name="deliver"
    )
    start_time = models.DateTimeField(
        auto_now_add=True, auto_now=False, null=True, blank=True
    )
    end_time = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )
    status = models.CharField(max_length=20, choices=STATUS_TYPE)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return " | ".join(
            [self.get_status, self.driver.full_name, self.order.user.full_name]
        )

    @property
    def time_total(self):
        "Calculate time left to deliver"
        return self.end_time - self.start_time

    @property
    def get_status(self):
        status_dict = dict(self.STATUS_TYPE)
        return status_dict[self.status]

    @property
    def get_time_diffrence(self):
        if self.status in [Deliver.PICKUP, Deliver.INWAY]:
            return int((datetime.now() - self.start_time).seconds / 60)

    def clean(self) -> None:
        if self.order:
            if self.order.receive_type not in [Order.DELIVER]:
                raise ValidationError({"order": "نوع تحویل سفارش انتخاب شده حضوری است"})
            if self.order.status not in [Order.DELIVERED, Order.DELIVERY]:
                raise ValidationError(
                    {
                        "order": "سفارش نمیتواند در وضعیت تحویل به پیک یا تحویل داده شده نباشد"
                    }
                )
        return super().clean()
