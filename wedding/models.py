from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class User(AbstractUser):
    preferred_name = models.CharField(max_length=50, blank=False, null=False)
    max_guests = models.IntegerField(
        blank=False,
        null=False,
        default=1,
        validators=[MaxValueValidator(10), MinValueValidator(1)],
    )
    is_rehearsal_guest = models.BooleanField(blank=False, null=False, default=False)


class Rsvp(models.Model):
    class Meta:
        verbose_name = "RSVP"
        verbose_name_plural = "RSVPs"

    guest = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, blank=False, null=False
    )

    coming = models.BooleanField(blank=False, null=False)

    # todo min, max
    num_guests = models.IntegerField(blank=False, null=False)

    note = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.guest.first_name}"


class RsvpSummary(Rsvp):
    class Meta:
        proxy = True
        verbose_name = "RSVP Summary"
        verbose_name_plural = "RSVPs Summary"


class Allergy(models.Model):
    class Meta:
        verbose_name_plural = "Allergies"

    ALLERGY_CHOICES = (
        ("celery", "Celery / Sellerie"),
        ("gluten", "Gluten"),
        ("crustaceans", "Crustaceans / Krebstiere"),
        ("eggs", "Eggs / Eier"),
        ("fish", "Fish / Fisch"),
        ("lupin", "Lupin / Lupine"),
        ("milk", "Milk / Milch"),
        ("molluscs", "Molluscs / Weichtiere"),
        ("mustard", "Mustard / Senf"),
        ("peanuts", "Peanuts / Erdnüsse"),
        ("sesame", "Sesame / Sesam"),
        ("soybeans", "Soy beans / Soja"),
        ("sulphur", "Sulphur dioxide / Schwefeldioxid"),
        ("nuts", "Tree nuts / Schalenfrüchte (Nüsse)"),
    )

    guest = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, blank=False, null=False
    )

    allergy = models.CharField(
        choices=ALLERGY_CHOICES, max_length=30, null=True, blank=True
    )


class AllergySummary(Allergy):
    class Meta:
        proxy = True
        verbose_name = "Allergy Summary"
        verbose_name_plural = "Allergies Summary"
