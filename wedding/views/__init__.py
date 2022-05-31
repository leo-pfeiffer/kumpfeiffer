from django.shortcuts import render
from django.views.generic import TemplateView

from .index import *


class IndexView(TemplateView):
    template_name = "index.html"

    def get(self, request, **kwargs):
        return render(request, self.template_name)
