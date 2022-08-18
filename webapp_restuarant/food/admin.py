from django.contrib import admin
from food.models import Food, FoodCategory

# Register your models here.
class FoodAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            return Food.objects.filter(restaurant__admin=request.user)


admin.site.register(Food, FoodAdmin)
admin.site.register(FoodCategory)  # Register your models here.
