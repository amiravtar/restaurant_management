from django.db import models


def food_directory_path(instance, filename):
    """_summary_
    Return a Path for Uploaded Food images
    Args:
        instance (Food): Created Food
        filename (str): Name of uploaded file

    Returns:
        str: Path for uploaded file
    """
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "foods/{0}/{0}_{1}.{2}".format(
        instance.id, "FoodImage", filename.split(".")[-1]
    )


def foodcategory_directory_path(instance, filename):
    """_summary_
    Return a Path for Uploaded FoodCategory images
    Args:
        instance (FoodCategory): Created FoodCategory
        filename (str): Name of uploaded file

    Returns:
        str: Path for uploaded file
    """
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "foodcategory/{0}/{0}+{1}.{2}".format(
        instance.id, "FoodCategoryImage", filename.split(".")[-1]
    )


class FoodCategory(models.Model):
    """_summary_
    Model to Hold Food diffrent cateorys
    """
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    image = models.FileField(
        null=True, blank=True, upload_to=foodcategory_directory_path
    )

    def __str__(self):
        return self.name

class Food(models.Model):
    """_summary_
    Model to Hold Foods
    """
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(
        "restaurant.Restaurant", on_delete=models.CASCADE, related_name="foods"
    )
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=food_directory_path,
        height_field=None,
        width_field=None,
        max_length=None,
    )

    def __str__(self):
        return " | ".join([self.name, self.restaurant.name])
