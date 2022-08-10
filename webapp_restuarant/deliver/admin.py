from ast import Del
from django.contrib import admin
from .models import Deliver
from order.models import Order

# Register your models here.


class DeliverAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "order":
            kwargs["queryset"] = Order.objects.filter(
                status__in=[Order.DELIVERED, Order.DELIVERY], receive_type=Order.DELIVER
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Deliver, DeliverAdmin)
