from urllib.request import Request
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views import View
from order.models import Order
from .forms import ProfileDetailForm, UserDetailForm, UserChangePassword


# Create your views here.
class Profile(View):
    template_name = "user/profile.html"
    frm_user = UserDetailForm
    frm_profile = ProfileDetailForm
    frm_password = UserChangePassword

    def get_forms(self, context, use_instance=True):
        frm_user = self.frm_user(instance=self.request.user, prefix="frm_user")
        frm_profile = self.frm_profile(
            instance=self.request.user.profile, prefix="frm_profile"
        )
        frm_password = self.frm_password(prefix="frm_password")

        context["frm_user"] = frm_user
        context["frm_profile"] = frm_profile
        context["frm_password"] = frm_password

    def get_orders(self, context):
        orders = Order.objects.filter(user__id=self.request.user.id).order_by(
            "-created_on"
        )
        context["orders"] = orders

    def get(self, request):
        context = {}
        self.get_forms(context)
        self.get_orders(context)
        context["user"] = request.user
        return render(request, self.template_name, context=context)

    def post(self, request):
        context = {}
        if "mode" in request.POST:
            if request.POST["mode"] == "edit_profile":
                frm_profile = self.frm_profile(
                    request.POST,
                    request.FILES,
                    instance=request.user.profile,
                    prefix="frm_profile",
                )
                if frm_profile.is_valid():
                    frm_profile.save()
                    messages.success(request, "باموفقیت ذخیره شد")
            if request.POST["mode"] == "edit_user":
                frm_user = self.frm_user(
                    request.POST, instance=request.user, prefix="frm_user"
                )
                if frm_user.is_valid():
                    frm_user.save()
                    messages.success(request, "باموفقیت ذخیره شد")
            if request.POST["mode"] == "edit_password":
                frm_password = self.frm_password(request.POST,prefix="frm_password")
                if frm_password.is_valid():
                    user = authenticate(
                        username=request.user.username,
                        password=frm_password.cleaned_data["oldpassword"],
                    )
                    if user is not None:
                        user.set_password(frm_password.cleaned_data["password2"])
                        user.save()
                        frm_password = self.frm_password()
                        messages.success(request, "رمز عبور شما تغیر یافت")
                        login(request, user)
                    else:
                        frm_password = self.frm_password()
                        frm_password.add_error(None, "رمز عبور قبلی اشتباه است")
                        messages.error(request, "رمز عبور قبلی اشتباه است")
                else:
                    print(frm_password.errors)
                    context["frm_password"] = frm_password
            self.get_forms(context)
            self.get_orders(context)
            return render(request, self.template_name, context=context)
