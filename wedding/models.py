from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Rsvp(models.Model):
    guest = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, blank=False, null=False
    )
    # todo min, max
    num_guests = models.IntegerField(blank=False, null=False)


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
        get_user_model(), on_delete=models.CASCADE, blank=False, null=False
    )

    allergy = models.CharField(choices=ALLERGY_CHOICES, max_length=30)
    note = models.CharField(max_length=200, null=True, blank=True)
