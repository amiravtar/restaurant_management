from django.shortcuts import render
from django.views import View

# Create your views here.


class Index(View):
    template_name = "prelogin/index.html"

    def get(self, request):
        return render(request, self.template_name)
