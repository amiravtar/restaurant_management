from django.shortcuts import render
from django.views import View
from order.models import Order

# Create your views here.
class Profile(View):
    template_name = "user/profile.html"

    def get(self, request):
        orders = Order.objects.filter(user__id=request.user.id).order_by("-created_on")
        return render(
            request,
            self.template_name,
            context={"user": request.user, "orders": orders},
        )
