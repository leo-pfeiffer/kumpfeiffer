from django import forms

from wedding.models import Rsvp


class RsvpForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.guests = kwargs.pop("guests", [])
        super().__init__(*args, **kwargs)
        css_class = "form-control form-opacity"

        for guest in self.guests:
            self.fields[guest["attending"]] = forms.ChoiceField(
                label=f"Is {guest['name']} attending?",
                choices=((True, "Yes"), (False, "No")),
                widget=forms.Select(attrs={"class": css_class}),
                required=True,
            )

            self.fields[guest["menu_first"]] = forms.ChoiceField(
                choices=Rsvp.FIRST_COURSE_CHOICES,
                label="First course",
                widget=forms.Select(attrs={"class": css_class}),
                required=True,
            )

            self.fields[guest["menu_second"]] = forms.ChoiceField(
                choices=Rsvp.SECOND_COURSE_CHOICES,
                label="Second course",
                widget=forms.Select(attrs={"class": css_class}),
                required=True,
            )

    # this is disgusting, but django made me do it :-(
    css_class = "form-control form-opacity"

    note = forms.CharField(
        label="Other Allergies / Notes",
        max_length=200,
        widget=forms.TextInput(attrs={"class": css_class}),
        required=False,
    )
