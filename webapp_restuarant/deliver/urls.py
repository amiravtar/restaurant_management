from django.urls import path
from .views import Index, Detail

app_name = "deliver"

urlpatterns = [
    path(
        "",
        Index.as_view(),
        name="Index",
    ),
    path(
        "details/<int:pk>",
        Detail.as_view(),
        name="Detail",
    ),
]
