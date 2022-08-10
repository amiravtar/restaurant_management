from django.db import models
from django.contrib.auth.models import User as djang_user
from django.urls import reverse_lazy

# Create your models here.


def user_directory_path(instance, filename):
    "Generate profile image path"
    # file will be uploaded to MEDIA_ROOT/user_<id>/<profile.format>
    print(filename.split("."))
    return "users/{0}/profile.{1}".format(instance.id, filename.split(".")[-1])


class User(djang_user):
    class Meta:
        proxy = True

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return self.get_full_name()


class Profile(models.Model):
    # user types
    ADMIN = "admin"
    ADMIN_RESTAURANT = "adminr"
    USER = "user"
    DRIVER = "driver"
    USER_TYPE = [
        (ADMIN, "admin"),
        (ADMIN_RESTAURANT, "adminb"),
        (USER, "user"),
        (DRIVER, "driver"),
    ]
    # related user obj
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    user_type = models.CharField(max_length=30, choices=USER_TYPE, default=USER)
    address = models.CharField(max_length=70, null=True, blank=True)
    nc = models.CharField(max_length=15)  # National Code
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=user_directory_path,
        height_field=None,
        width_field=None,
        max_length=None,
    )
    phone = models.CharField(max_length=12, null=True, blank=True)
    temp_order = models.OneToOneField(
        "order.Order",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="temp_user",
    )

    def __str__(self):
        return " | ".join([self.full_name, self.user_type])

    @property
    def full_name(self) -> str:
        return self.user.get_full_name()

    @property
    def is_special_type(self):
        return self.user_type in [
            Profile.ADMIN,
            Profile.ADMIN_RESTAURANT,
            Profile.DRIVER,
        ]

    @property
    def get_special_url(self):
        if self.user_type in [Profile.ADMIN, Profile.ADMIN_RESTAURANT]:
            return reverse_lazy("admin:index")
        elif self.user_type == Profile.DRIVER:
            return reverse_lazy("deliver:Index")

    @property
    def get_special_string(self):
        if self.user_type in [Profile.ADMIN, Profile.ADMIN_RESTAURANT]:
            return "پنل مدیر"
        elif self.user_type == Profile.DRIVER:
            return "پنل پیک"

    def clear_temp(self):
        self.temp_order = None
        self.save()
