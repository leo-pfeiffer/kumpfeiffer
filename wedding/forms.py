from django import forms

from wedding.models import Allergy


class RsvpForm(forms.Form):

    # this is disgusting, but django made me do it :-(
    css_class = "shadow appearance-none border rounded py-1 px-1 text-gray-700"

    num_guests = forms.IntegerField(
        label="Number of guests",
        widget=forms.NumberInput(attrs={'class': css_class + " w-full"})
    )
    allergies = forms.MultipleChoiceField(
        choices=Allergy.ALLERGY_CHOICES,
        label="Allergies",
        widget=forms.CheckboxSelectMultiple(attrs={'class': css_class}),
        required=False
    )
    note = forms.CharField(
        label="Other Allergies / Notes",
        max_length=200,
        widget=forms.TextInput(attrs={'class': css_class + " w-full"}),
        required=False
    )


