from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from wedding.forms import RsvpForm


class HomeView(TemplateView):
    template_name = "home.html"

    def get(self, request, **kwargs):
        return render(request, self.template_name, {
            'form': RsvpForm()
        })

    def post(self, request, *args, **kwargs):
        form = RsvpForm(request.POST)
        if form.is_valid():
            # todo do something with with the form
            #  - check if guest already RSVP'd
            #  - if no, save rsvp and allergies
            #  - if yes, redirect and complain
            return HttpResponseRedirect('/thanks')

        return render(request, self.template_name, {
            'form': form
        })