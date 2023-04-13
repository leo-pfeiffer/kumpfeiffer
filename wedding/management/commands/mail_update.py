from django.core.management.base import BaseCommand

from wedding.mailer import Mailer
from wedding.utils import get_email_update


class Command(BaseCommand):
    """
    Usage:
    python manage.py mail_update [--all]
    """

    def add_arguments(self, parser):
        parser.add_argument("--all", action="store_true", default=False, dest="all")

    def handle(self, *args, **kwargs):
        send_to_all = kwargs["all"]
        msg = get_email_update()

        all_emails = [
            "leopold.pfeiffer@icloud.com",
            "tinatyson@me.com",
            "pkumpf@me.com",
            "ktkumpf@me.com",
        ]

        just_me = ["leopold.pfeiffer@icloud.com"]

        print("Sending update to", all_emails if send_to_all else just_me, sep="\n")

        Mailer().send_mail(
            all_emails if send_to_all else just_me, "RSVP status update", msg
        )
