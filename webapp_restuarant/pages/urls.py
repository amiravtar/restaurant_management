from django.urls import path
from .views import Index

app_name = "pages"

urlpatterns = [
    path(
        "",
        Index.as_view(),
        name="Index",
    ),
]
