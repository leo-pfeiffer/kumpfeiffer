from django.shortcuts import render
from django.views.generic import TemplateView


class SaveTheDateView(TemplateView):
    template_name = "save_the_date.html"

    def get(self, request, **kwargs):
        return render(request, self.template_name)
