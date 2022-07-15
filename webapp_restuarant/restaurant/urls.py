from django.urls import path
from .views import Checkout, List, Menu

app_name = "restaurant"

urlpatterns = [
    path("checkout/", Checkout.as_view(), name="Checkout"),
    # List all restaurants
    path("list/", List.as_view(), name="Index"),
    #
    path("list/menu/<int:pk>", Menu.as_view(), name="Menu"),
]
