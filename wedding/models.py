from django.db import models

from wedding.utils import invite_code_generator


class Guest(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    invite_code = models.CharField(
        max_length=6, default=invite_code_generator, unique=True)

    def __str__(self):
        return f"{self.name}"


class Rsvp(models.Model):
    guest = models.ForeignKey(
        Guest, on_delete=models.CASCADE, blank=False, null=False
    )
    # todo min, max
    num_guests = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return f"{self.guest.name}"


class Allergy(models.Model):
    ALLERGY_CHOICES = (
        ('celery', 'Celery / Sellerie'),
        ('gluten', 'Gluten'),
        ('crustaceans', 'Crustaceans / Krebstiere'),
        ('eggs', 'Eggs / Eier'),
        ('fish', 'Fish / Fisch'),
        ('lupin', 'Lupin / Lupine'),
        ('milk', 'Milk / Milch'),
        ('molluscs', 'Molluscs / Weichtiere'),
        ('mustard', 'Mustard / Senf'),
        ('peanuts', 'Peanuts / Erdnüsse'),
        ('sesame', 'Sesame / Sesam'),
        ('soybeans', 'Soy beans / Soja'),
        ('sulphur', 'Sulphur dioxide / Schwefeldioxid'),
        ('nuts', 'Tree nuts / Schalenfrüchte (Nüsse)'),
    )

    guest = models.ForeignKey(
        Guest, on_delete=models.CASCADE, blank=False, null=False
    )

    allergy = models.CharField(choices=ALLERGY_CHOICES, max_length=30)
    note = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.guest.name}: {self.allergy}"
