from django import forms

from wedding.models import Allergy


class RsvpForm(forms.Form):

    def __init__(self, *args, **kwargs):
        max_guests = kwargs.pop("max_guests")
        super().__init__(*args, **kwargs)
        css_class = "form-control form-opacity"

        self.fields['num_guests'] = forms.IntegerField(
            label="Number of guests",
            min_value=0,
            max_value=max_guests,
            widget=forms.NumberInput(attrs={'class': css_class})
        )

    # this is disgusting, but django made me do it :-(
    css_class = "form-control form-opacity"

    TRUE_FALSE_CHOICES = (
        (True, 'Yes'),
        (False, 'No')
    )

    coming = forms.ChoiceField(choices=TRUE_FALSE_CHOICES,
                                  label="Will you attend?",
                                  initial='',
                                  widget=forms.Select(attrs={'class': css_class}),
                                  required=True)

    allergies = forms.MultipleChoiceField(
        choices=Allergy.ALLERGY_CHOICES,
        label="Allergies",
        widget=forms.CheckboxSelectMultiple(attrs={'class': ""}),
        required=False
    )
    note = forms.CharField(
        label="Other Allergies / Notes",
        max_length=200,
        widget=forms.TextInput(attrs={'class': css_class}),
        required=False
    )


