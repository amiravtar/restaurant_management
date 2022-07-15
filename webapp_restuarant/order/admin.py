from django.contrib import admin
from order.models import FoodCount, Order, OrderDate, DateFoodCount
from jalali_date.admin import ModelAdminJalaliMixin
from jalali_date import datetime2jalali, date2jalali
from utils.date_persian import date_fromgregorian
import logging

# Register your models here.
logger = logging.getLogger("app")


@admin.action(description="Get Order Date for orders")
def get_order_date(modeladmin, request, queryset):
    for obj in queryset:
        if not obj.get_order_date():
            logger.warning("Coudnt get order_date for order {0}".format(obj.id))


class OrderAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = [
        "get_created_jalali",
        "user",
        "status",
        "restaurant",
        "get_target_date_jalali",
    ]
    ordering = ["created_on", "target_date"]
    actions = [get_order_date]
    date_hierarchy = (
        "created_on"  # Show order by date base of this fields on top of page
    )
    list_editable = ["status"]  # List of editable orders in view mode

    @admin.display(description="تاریخ ایجاد سفارش", ordering="created_on")
    def get_created_jalali(self, obj):
        return date_fromgregorian(obj.created_on).strftime("%Y/%m/%d %H:%M:%S %b %a")

    @admin.display(description="تاریخ تحویل", ordering="target_date")
    def get_target_date_jalali(self, obj):
        return date_fromgregorian(obj.target_date).strftime("%Y/%m/%d %b %a")


admin.site.register(Order, OrderAdmin)
admin.site.register(FoodCount)
admin.site.register(OrderDate)
admin.site.register(DateFoodCount)
