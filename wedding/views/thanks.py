from django.shortcuts import render
from django.views.generic import TemplateView


class ThanksView(TemplateView):
    template_name = "thanks.html"

    def get(self, request, **kwargs):
        return render(request, self.template_name)