from django import forms
from wedding.models import Allergy


class RsvpForm(forms.Form):
    num_guests = forms.IntegerField(label="Number of guests")
    allergies = forms.MultipleChoiceField(choices=Allergy.ALLERGY_CHOICES)

