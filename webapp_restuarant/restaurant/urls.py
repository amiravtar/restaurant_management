from django.urls import path
from .views import Checkout, List

app_name = "restaurant"

urlpatterns = [
    path("checkout/", Checkout.as_view(), name="Checkout"),
    path("list/", List.as_view(), name="Index"),
]
