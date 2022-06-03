from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    invite_code = models.CharField(max_length=4)


class Rsvp(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False
    )
    # todo min, max
    guests = models.IntegerField(blank=False, null=False)


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

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False
    )

    allergy = models.CharField(choices=ALLERGY_CHOICES, max_length=30)
    note = models.CharField(max_length=200)
