from django.db import models


# Create your models here.
class Deliver(models.Model):
    INWAY = "inway"
    PICKUP = "pickup"
    DELIVERD = "deliverd"
    NDELIVERD = "ndeliverd"
    STATUS_TYPE = [
        (INWAY, "در راه"),
        (PICKUP, "در حال دریافت از رستوران"),
        (DELIVERD, "تحویل داده شده"),
        (NDELIVERD, "تحویل داده نشده"),
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
            [self.status, self.driver.FullName, self.order.user.full_name]
        )

    @property
    def time_total(self):
        "Calculate time left to deliver"
        return self.end_time - self.start_time

    def get_status(self):
        status_dict = dict(self.STATUS_TYPE)
        return status_dict[self.status]
