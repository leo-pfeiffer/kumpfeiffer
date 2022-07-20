from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from wedding.utils import read_guest_csv, generate_invite_code, save_guest_list_rows


class Command(BaseCommand):
    """
    Example usage:
    python manage.py import_guest_csv "resources/guests.csv"
    """

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs["path"]
        self.import_guest_csv(path)

    @staticmethod
    def import_guest_csv(path):
        rows = read_guest_csv(path)

        # create users
        save_guest_list_rows(rows)
