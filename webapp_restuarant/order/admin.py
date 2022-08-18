from django.contrib import admin
from order.models import FoodCount, Order, OrderDate, DateFoodCount, FixMenu
from food.models import Food
from restaurant.models import Restaurant
from jalali_date.admin import ModelAdminJalaliMixin
from utils.date_persian import date_fromgregorian
from django.db.models import Q
import logging

# Register your models here.
logger = logging.getLogger("app")


@admin.action(description="Get Order Date for orders")
def get_order_date(modeladmin, request, queryset):
    for obj in queryset:
        if not obj.get_order_date():
            logger.warning("Coudnt get order_date for order {0}".format(obj.id))


class OrderDateFoodsInline(admin.TabularInline):
    model = OrderDate.foods.through
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "datefoodcount":
            if "object_id" in request.resolver_match.kwargs:
                kwargs["queryset"] = DateFoodCount.objects.filter(
                    Q(order_date__isnull=True)
                    | Q(order_date__id=request.resolver_match.kwargs["object_id"])
                )
            else:
                kwargs["queryset"] = DateFoodCount.objects.filter(
                    Q(order_date__isnull=True)
                )
        q = super().formfield_for_foreignkey(db_field, request, **kwargs)
        return q


class OrderDateAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    inlines = [OrderDateFoodsInline]
    exclude = ["foods"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "fix_menu":
            if "object_id" in request.resolver_match.kwargs:
                obj_id = request.resolver_match.kwargs["object_id"]
                kwargs["queryset"] = FixMenu.objects.filter(
                    restaurant__id=OrderDate.objects.get(id=obj_id).restaurant.id
                )
            else:
                kwargs["queryset"] = FixMenu.objects.filter(
                    restaurant__admin=request.user
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            return OrderDate.objects.filter(restaurant__admin=request.user)


class FixMenuFoodsInline(admin.TabularInline):
    model = FixMenu.foods.through
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "food":
            if not request.user.is_superuser:
                kwargs["queryset"] = Food.objects.filter(restaurant__admin=request.user)
            return super().formfield_for_foreignkey(
                db_field=db_field, request=request, **kwargs
            )


class FixMenuAdmin(admin.ModelAdmin):
    inlines = [FixMenuFoodsInline]
    exclude = ["foods"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "restaurant":
            if not request.user.is_superuser:
                kwargs["queryset"] = Restaurant.objects.filter(admin=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            return FixMenu.objects.filter(restaurant__admin=request.user)


class OrderAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = [
        "get_created_jalali",
        "user",
        "status",
        "restaurant",
        "get_target_date_jalali",
    ]
    ordering = ["-created_on", "target_date"]
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

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            return Order.objects.filter(restaurant__admin=request.user)

class DateFoodCountAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "food":
            if not request.user.is_superuser:
                kwargs["queryset"] = Food.objects.filter(restaurant__admin=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Order, OrderAdmin)
admin.site.register(FoodCount)
admin.site.register(OrderDate, OrderDateAdmin)
admin.site.register(DateFoodCount, DateFoodCountAdmin)
admin.site.register(FixMenu, FixMenuAdmin)
