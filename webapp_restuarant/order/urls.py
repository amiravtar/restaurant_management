from django.urls import path
from .views import Status

app_name = "order"

urlpatterns = [
    path("status/<int:pk>", Status.as_view(), name="Status"),
]
