from datetime import datetime
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.contrib import messages

from order.models import Order
from .models import Deliver


# Create your views here.
class Index(ListView):
    template_name = "deliver/index.html"
    model = Deliver
    context_object_name = "delivers"

    def get_queryset(self):
        return Deliver.objects.filter(
            driver__user=self.request.user,
            status__in=[Deliver.INWAY, Deliver.PICKUP],
        )


class Detail(DetailView):
    template_name = "deliver/detail.html"
    context_object_name = "order"
    model = Deliver

    def get_object(self):
        deliver = get_object_or_404(Deliver, pk=self.kwargs["pk"])
        return deliver.order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["deliver"] = get_object_or_404(Deliver, pk=self.kwargs["pk"])
        return context

    def post(self, request, pk):
        deliver = get_object_or_404(Deliver, pk=pk)
        if "action" in request.POST and "description" in request.POST:
            if request.POST["action"] == "delivered":
                deliver.status = Deliver.DELIVERD
                deliver.description = request.POST["description"]
                deliver.order.status = Order.DELIVERED
                deliver.end_time = datetime.now()
                deliver.save()
                deliver.order.save()
                messages.success(
                    request,
                    "با موفقیت ثبت شد",
                )
                return JsonResponse(
                    {"response": "success", "redirect": reverse_lazy("deliver:Index")}
                )
            else:
                if len(request.POST["description"]) < 15:
                    return JsonResponse(
                        {
                            "response": "error",
                            "error": "حداقل توضیحات برای تحویل ندادن سفارش باید ۱۵ حرف باشد",
                        }
                    )
                deliver.status = Deliver.NDELIVERD
                deliver.description = request.POST["description"]
                deliver.order.status = Order.FAILED
                deliver.save()
                deliver.order.save()
                messages.warning(
                    request,
                    "تحویل داده نشدن سفارش ثبت شد.لطفا هرچه سریع تر با رستوران تماس بگیرید",
                )
                return JsonResponse(
                    {"response": "success", "redirect": reverse_lazy("deliver:Index")}
                )
        else:
            return Http404
