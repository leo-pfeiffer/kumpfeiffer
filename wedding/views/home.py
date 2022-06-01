from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"

    def get(self, request, **kwargs):
        return render(request, self.template_name)