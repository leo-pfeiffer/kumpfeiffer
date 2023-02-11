import requests
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import Q

from wedding.models import Guest, Rsvp


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        total_users = get_user_model().objects.filter(~Q(username="admin")).count()
        total_guests = Guest.objects.count()
        total_rsvp = Rsvp.objects.count()
        rsvp_coming = Rsvp.objects.filter(coming=False).count()
        ntfy_msg = f"Here's your update:\n" \
                   f"Total users: {total_users}\n" \
                   f"Total guests: {total_guests}\n" \
                   f"Total RSVPs: {total_rsvp}\n" \
                   f"    Coming: {rsvp_coming}\n" \
                   f"    Not coming: {total_rsvp - rsvp_coming}"

        requests.post("https://ntfy.sh/kumpfeiffer-rsvp", data=ntfy_msg)
