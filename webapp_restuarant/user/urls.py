from django.urls import path
from django.contrib.auth import views as auth_views
from .views import Profile

app_name = "user"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="user/login.html", redirect_authenticated_user=True
        ),
        name="Login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="user/login.html"),
        name="Logout",
    ),
    path(
        "logout/",
        auth_views.PasswordResetDoneView.as_view(template_name="user/login.html"),
        name="PassowrdReset",
    ),
    path("profile/", Profile.as_view(), name="Profile"),
]
