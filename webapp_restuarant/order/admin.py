from django.contrib import admin
from order.models import FoodCount, Order, OrderDate, DateFoodCount
import logging

# Register your models here.
logger = logging.getLogger("app")


@admin.action(description="Get Order_Date for orders")
def get_order_date(modeladmin, request, queryset):
    for obj in queryset:
        if not obj.get_order_date():
            logger.warning("Coudnt get order_date for order {0}".format(obj.id))


class OrderAdmin(admin.ModelAdmin):
    list_display = ["created_on", "target_date", "user", "status", "restaurant"]
    ordering = ["created_on", "target_date"]
    actions = [get_order_date]


admin.site.register(Order, OrderAdmin)
admin.site.register(FoodCount)
admin.site.register(OrderDate)
admin.site.register(DateFoodCount)
