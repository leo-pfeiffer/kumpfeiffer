from django.shortcuts import render
from django.views.generic import TemplateView


class LangsView(TemplateView):
    template_name = "langs.html"

    def get(self, request, **kwargs):
        return render(request, self.template_name)
