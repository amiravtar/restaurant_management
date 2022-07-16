from django.shortcuts import get_object_or_404, render
from django.views import View

from order.models import Order

# Create your views here.
class Status(View):
    template_name = "order/status.html"

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user__id=request.user.id)

        return render(request, self.template_name, context={"order": order})
