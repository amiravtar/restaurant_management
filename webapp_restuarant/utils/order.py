from order.models import FoodCount
from order.models import Order
from datetime import timedelta
from django.utils import timezone


def get_or_create_order_food(food, count):
    order_food = None
    try:
        order_food = FoodCount.objects.get(food=food, count=count)
    except:
        order_food = FoodCount.objects.create(food=food, count=count)

    return order_food


ORDER_TEMP_TIME = 10


def get_session_order(request, delete=False):
    try:
        id = request.session.get("order_data", None)
        if id:
            order = Order.objects.filter(pk=id, user__id=request.user.id)
            if not order.exists():
                del request.session["order_data"]
                return None
            if order.exists():
                if order[0].status != Order.TEMP:
                    del request.session["order_data"]
                    return None
                if order[0].created_on < timezone.now() - timedelta(
                    minutes=ORDER_TEMP_TIME
                ):
                    del request.session["order_data"]
                    order[0].delete()
                    return None
                else:
                    if delete:
                        del request.session["order_data"]
                    return order[0]

            else:
                del request.session["order_data"]
        else:
            order = Order.objects.filter(
                status__in=[Order.TEMP],
                user__id=request.user.id,
            )
            if order.exists():
                if order[0].created_on < timezone.now() - timedelta(
                    minutes=ORDER_TEMP_TIME
                ):
                    order[0].delete()
                    return None
                request.session["order_data"] = order[0].id
                return order[0]
    except Exception as e:
        print(e)
        return None
