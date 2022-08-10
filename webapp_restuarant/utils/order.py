from order.models import FoodCount
from order.models import Order
from datetime import timedelta
from django.utils import timezone
import logging

logger = logging.getLogger("app")


def get_or_create_order_food(food, count):
    order_food = None
    try:
        order_food = FoodCount.objects.get(food=food, count=count)
    except Exception as e:
        logger.info(e)
        order_food = FoodCount.objects.create(food=food, count=count)
    return order_food


ORDER_TEMP_TIME = 10


def get_session_order(request, delete=False):
    try:
        profile = request.user.profile
        if profile.temp_order:
            if profile.temp_order.created_on < timezone.now() - timedelta(
                minutes=ORDER_TEMP_TIME
            ):
                profile.temp_order.delete()
                profile.temp_order = None
                profile.save()
                return None
            else:
                return profile.temp_order
        else:
            return None
    except Exception as e:
        print(e)
        return None
