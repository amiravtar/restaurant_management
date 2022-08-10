import json
from pprint import pprint
from sre_constants import SUCCESS
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from food.models import Food
from .models import Restaurant
from order.models import DateFoodCount, Order, OrderDate
from django.contrib import messages
from utils.order import get_or_create_order_food, get_session_order
import datetime as py_datetime
import logging

# Create your views here.

logger = logging.getLogger("app")


class Checkout(View):
    template_name = "restaurant/checkout.html"

    def get(self, request):
        order = get_session_order(request)
        if not order:
            return redirect("restaurant:Index")
        return render(request, self.template_name, context={"order": order})

    def post(self, request):
        order = get_session_order(request)
        if not order:
            return JsonResponse(
                {
                    "response": "error",
                    "redirect": reverse_lazy("restaurant:Index"),
                    "error": "زمان تایید سفارش شما به اتمام رسیده",
                }
            )
        if "resive_type" in request.POST and "order_address" in request.POST:
            order.address = request.POST["order_address"]
            order.resive_type = (
                Order.TAKEOUT
                if request.POST["resive_type"] == "takeout"
                else Order.DELIVER
            )
            order.status = Order.PENDING_CONFIRM
            order.save()
            self.request.user.profile.clear_temp()
            return JsonResponse(
                {
                    "response": "success",
                    "redirect": reverse_lazy("order:Status", kwargs={"pk": order.pk}),
                }
            )
        else:
            if "resive_type_change" in request.POST:
                order.receive_type = (
                    Order.TAKEOUT
                    if request.POST["resive_type"] == "takeout"
                    else Order.DELIVER
                )
                order.save()
                return JsonResponse(
                    {
                        "response": "success",
                    }
                )
            else:
                return JsonResponse(
                    {
                        "response": "error",
                        "redirect": reverse_lazy("restaurant:Checkout"),
                        "error": "لطفا آدرس و نحوه دریافت را مشخص کنید",
                    }
                )


class List(LoginRequiredMixin, ListView):
    template_name = "restaurant/list.html"
    model = Restaurant
    resturants_list = Restaurant.objects.all()
    paginate_by = 3


class Menu(LoginRequiredMixin, View):
    template_name = "restaurant/menu.html"

    def get_order_dates(self, restaurant):
        date_orders = OrderDate.objects.filter(
            date__range=(
                py_datetime.date.today(),
                py_datetime.timedelta(days=restaurant.max_reserve_time)
                + py_datetime.date.today(),
            ),
            restaurant=restaurant,
        )
        return date_orders

    def foods_from_order_date(self, order_date):
        data = {}
        for i in order_date.foods.all():
            data.setdefault(
                i.food.category.id, {"cate_name": i.food.category.name, "foods": []}
            )["foods"].append(
                {
                    "count": i.count,
                    "food": {
                        "id": i.food.id,
                        "name": i.food.name,
                        "price": i.food.price,
                        "des": i.food.description,
                        "image": i.food.image.url if i.food.image else None,
                    },
                }
            )
        if order_date.fix_menu:
            for i in order_date.fix_menu.foods.all():
                data.setdefault(
                    i.category.id, {"cate_name": i.category.name, "foods": []}
                )["foods"].append(
                    {
                        "count": 999,
                        "food": {
                            "id": i.id,
                            "name": i.name,
                            "price": i.price,
                            "des": i.description,
                            "image": i.image.url if i.image else None,
                        },
                    }
                )
        return data

    def check_foods_with_order_date(self, order_date: OrderDate, data: dict):
        # return order if success
        order: Order = Order.objects.create(
            user=self.request.user,
            restaurant=order_date.restaurant,
            receive_type=Order.TAKEOUT,
            status=Order.TEMP,
            description=data["description"],
            target_date=order_date.date,
            order_date=order_date,
        )
        for i in data["foods"]:
            food = Food.objects.filter(pk=i)
            if not food.exists():
                messages.error(self.request, "غذای مورد نظر وجود ندارد")
                return None
            food = food[0]
            fc = order_date.foods.filter(food=food)
            if not fc.exists():
                if order_date.fix_menu and order_date.fix_menu.foods.contains(food):
                    fc = food
                else:
                    messages.error(
                        self.request, "غذای مورد نظر برای این روز وجود ندارد"
                    )
                    return None
            if not type(fc) == Food:
                fc = fc[0]
                if data["foods"][i]["count"] > fc.count:
                    messages.error(
                        self.request,
                        "تعداد سفارش برای غذای {0} بیشتر از مقدار مجاز است".format(
                            food.name
                        ),
                    )
                    return None
            order_food_count = get_or_create_order_food(food, data["foods"][i]["count"])
            order.foods.add(order_food_count)
        order.save()
        profile = self.request.user.profile
        if profile.temp_order:
            profile.temp_order.delete()
        profile.temp_order = order
        profile.save()
        return order

    def reduce_date_order_food(self, order: Order):
        if order.order_date == None:
            raise ValidationError("سفارش انتخابی تاریخ مرجعی ندارد")
        order_date = order.order_date
        dfcs = DateFoodCount.objects.filter(order_date__id=order_date.id)
        for fc in order.foods.all():
            df = dfcs.filter(food=fc.food)
            if df.exists():
                df = df[0]
            else:
                if order_date.fix_menu and order_date.fix_menu.foods.contains(fc.food):
                    continue
                else:
                    logger.error(
                        "DateFoodCount with food {0} Dosent exist for this order {1}".format(
                            fc.food, order.id
                        )
                    )
                    raise ValidationError("غذای مورد نظر پیدا نشد")
            df.count = df.count - fc.count
            df.save()

    def get(self, request, pk):
        restaurant = get_object_or_404(Restaurant, pk=pk)
        order_dates = self.get_order_dates(restaurant)
        # order = get_session_order(request)
        context = {"restaurant": restaurant, "order_dates": order_dates}
        # context["order"] = order if order else None
        return render(
            request,
            self.template_name,
            context=context,
        )

    def post(self, request, pk):
        if "mod" in request.POST:
            if request.POST["mod"] == "send_date":
                order_date = get_object_or_404(OrderDate, pk=request.POST["date"])
                foods = self.foods_from_order_date(order_date)
                return JsonResponse(
                    {
                        "response": "success",
                        "data": json.dumps(foods, ensure_ascii=False),
                    }
                )
            elif request.POST["mod"] == "checkout":
                data = json.loads(request.POST["data"])
                order_date = get_object_or_404(OrderDate, pk=request.POST["date"])
                order = self.check_foods_with_order_date(order_date, data)
                if order is not None:
                    self.reduce_date_order_food(order)
                    return JsonResponse(
                        {
                            "response": "success",
                            "redirect": reverse_lazy("restaurant:Checkout"),
                        }
                    )
                else:
                    return JsonResponse({"response": "error"})
