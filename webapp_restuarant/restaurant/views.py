from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Restaurant
# Create your views here.


class Checkout(View):
    pass


class List(LoginRequiredMixin, ListView):
    template_name = "restaurant/list.html"
    model = Restaurant
    resturants_list = Restaurant.objects.all()
    paginate_by = 3
