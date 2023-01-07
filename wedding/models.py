from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class User(AbstractUser):
    """
    This model represents both a user of the application and a single invite
    sent out. Each invite has at least one actual "Guest" associated with it, or more
    if the invite is for more than one person.
    """

    is_rehearsal_guest = models.BooleanField(blank=False, null=False, default=False)


class Guest(models.Model):
    """
    This represents and actual "Guest" that is invited. Each guest is associated with
    a single "User" (invite) and has a single "RSVP" associated with it.
    """

    primary_guest = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, blank=False, null=False
    )
    name = models.CharField(max_length=50, blank=False, null=False)


class Rsvp(models.Model):
    """
    This represents the "RSVP" for a single "Guest". Each "Guest" has a single "RSVP"
    associated with it.
    """

    class Meta:
        verbose_name = "RSVP"
        verbose_name_plural = "RSVPs"

    # todo update choices
    FIRST_COURSE_CHOICES = [
        ("chicken", "Chicken"),
        ("fish", "Fish"),
    ]

    # todo update choices
    SECOND_COURSE_CHOICES = [
        ("chicken", "Chicken"),
        ("fish", "Fish"),
    ]

    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, blank=False, null=False)

    coming = models.BooleanField(blank=False, null=False)

    note = models.CharField(max_length=200, null=True, blank=True)

    first_course = models.CharField(
        max_length=50, choices=FIRST_COURSE_CHOICES, blank=False, null=False
    )

    second_course = models.CharField(
        max_length=50, choices=SECOND_COURSE_CHOICES, blank=False, null=False
    )

    def __str__(self):
        return f"{self.guest.first_name}"


class RsvpSummary(Rsvp):
    class Meta:
        proxy = True
        verbose_name = "RSVP Summary"
        verbose_name_plural = "RSVPs Summary"
