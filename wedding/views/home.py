from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from wedding.forms import RsvpForm
from wedding.models import Rsvp, Guest


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def render_default(self, request):

        user = request.user
        has_rsvp = Rsvp.objects.filter(guest__primary_guest=user).exists()
        rsvp = {}
        note = None
        if has_rsvp:
            rsvp_objs = Rsvp.objects.filter(guest__primary_guest=user).all()
            rsvp = []
            for rsvp_obj in rsvp_objs:
                rsvp.append(
                    {
                        "name": rsvp_obj.guest.name,
                        "coming": "Yes" if rsvp_obj.coming else "No",
                        "first_course": rsvp_obj.first_course,
                        "second_course": rsvp_obj.second_course,
                    }
                )
            note = rsvp_objs[0].note

        return render(
            request,
            self.template_name,
            {
                "form": RsvpForm(guests=self.create_guest_list(user)),
                "invite_code": user.username,
                "name": user.first_name,
                "has_rsvp": Rsvp.objects.filter(
                    guest__primary_guest=request.user
                ).exists(),
                "rsvp": rsvp,
                "note": note,
                "is_rehearsal_guest": user.is_rehearsal_guest,
                "guests": self.create_guest_list(user),
            },
        )

    def get(self, request, **kwargs):
        return self.render_default(request)

    def post(self, request, *args, **kwargs):
        form = RsvpForm(
            request.POST,
            guests=self.create_guest_list(request.user),
        )
        if form.is_valid():

            # user has already RSVP'd -> shouldn't even get here
            if Rsvp.objects.filter(guest__primary_guest=request.user).exists():
                print("user already has rsvp")
                return render(
                    request,
                    self.template_name,
                    {
                        "form": RsvpForm(guests=self.create_guest_list(request.user)),
                        "invite_code": request.user.username,
                        "name": request.user.first_name,
                    },
                )

            for guest in form.guests:
                rsvp = Rsvp(
                    guest=Guest.objects.get(pk=guest["id"]),
                    coming=form.cleaned_data[guest["attending"]],
                    note=form.cleaned_data["note"],
                    first_course=form.cleaned_data[guest["menu_first"]],
                    second_course=form.cleaned_data[guest["menu_second"]],
                )

                rsvp.save()

            return HttpResponseRedirect("/thanks")

        return self.render_default(request)

    @staticmethod
    def create_guest_list(user):
        guests = list(Guest.objects.filter(primary_guest=user).values())
        for guest in guests:
            guest["attending"] = f"attending_{guest['id']}"
            guest["menu_first"] = f"menu_first_{guest['id']}"
            guest["menu_second"] = f"menu_second_{guest['id']}"
        return guests
