from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from wedding.forms import RsvpForm
from wedding.models import Rsvp, Allergy


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def render_default(self, request):

        user = request.user
        has_rsvp = Rsvp.objects.filter(guest=user).exists()
        rsvp = {}
        if has_rsvp:
            rsvp_obj = Rsvp.objects.filter(guest=user).first()
            rsvp = {
                "num_guests": rsvp_obj.num_guests,
                "note": rsvp_obj.note,
                "allergies": Allergy.objects.filter(guest=user)
                    .values_list("allergy", flat=True)
            }

        return render(request, self.template_name, {
            'form': RsvpForm(),
            "invite_code": user.username,
            "name": user.first_name,
            "has_rsvp": Rsvp.objects.filter(guest=request.user).exists(),
            "rsvp": rsvp
        })

    def get(self, request, **kwargs):
        return self.render_default(request)

    def post(self, request, *args, **kwargs):
        form = RsvpForm(request.POST)
        if form.is_valid():

            # user has already RSVP'd -> shouldn't even get here
            if Rsvp.objects.filter(guest=request.user).exists():
                print("user already has rsvp")
                return render(request, self.template_name, {
                    'form': RsvpForm(),
                    "invite_code": request.user.username,
                    "name": request.user.first_name
                })

            rsvp = Rsvp(
                guest=request.user,
                num_guests=form.cleaned_data['num_guests'],
                note=form.cleaned_data['note']
            )

            rsvp.save()

            for allergy in form.cleaned_data['allergies']:
                a = Allergy(guest=request.user, allergy=allergy)
                a.save()

            return HttpResponseRedirect('/thanks')

        return self.render_default(request)
