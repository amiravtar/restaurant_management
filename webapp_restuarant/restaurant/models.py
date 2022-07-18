from django.db import models
from django.urls import reverse_lazy


def restaurant_directory_path(instance, filename):
    "Generate restaurant image path"
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "restaurants/{0}/{0}_profile.{1}".format(
        instance.id, filename.split(".")[-1]
    )


# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=restaurant_directory_path,
        height_field=None,
        width_field=None,
        max_length=None,
    )
    admin = models.OneToOneField(
        "user.User", on_delete=models.CASCADE, related_name="restaurant"
    )
    address = models.CharField(max_length=80)
    phone = models.CharField(max_length=12)
    deliver_fee = models.IntegerField(null=True, blank=True, default=0)
    is_delivery_available = models.BooleanField(default=False)
    is_open = models.BooleanField(default=False)
    open_hour = models.TimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )
    close_hour = models.TimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("restaurant:Menu", kwargs={"pk": self.pk})

    @property
    def get_foods_category(self):
        di = set()
        if self.foods:
            for i in self.foods.all():
                di.add(i.category.name)
        return " , ".join(di)

    @property
    def get_open_hour(self):
        if self.open_hour:
            return self.open_hour.strftime("%H:%M")

    @property
    def get_close_hour(self):
        if self.close_hour:
            return self.close_hour.strftime("%H:%M")

    @property
    def get_foods_category_list(self):
        di = set()
        if self.foods:
            for i in self.foods.all():
                di.add(i.category)
        return di


class Driver(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=False)

    @property
    def full_name(self):
        return self.user.get_full_name()

    def __str__(self):
        return " | ".join([self.full_name, self.restaurant.name])

