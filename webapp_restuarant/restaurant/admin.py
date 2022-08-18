from django.contrib import admin
from .models import Restaurant, Driver


class RestaurantAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            return Restaurant.objects.filter(admin=request.user)


class DriverAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            return Driver.objects.filter(restaurant__admin=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "restaurant":
            if not request.user.is_superuser:
                kwargs["queryset"] = Restaurant.objects.filter(admin=request.user)
            return super().formfield_for_foreignkey(
                db_field=db_field, request=request, **kwargs
            )


# Register your models here.
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Driver, DriverAdmin)
