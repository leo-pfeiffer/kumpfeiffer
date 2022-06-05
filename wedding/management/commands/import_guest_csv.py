from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from wedding.utils import read_guest_csv, generate_invite_code


class Command(BaseCommand):
    """
    Example usage:
    python manage.py import_guest_csv "kumpfeiffer/fixtures/test_guests.csv"
    """

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs["path"]
        self.import_guest_csv(path)

    @staticmethod
    def import_guest_csv(path):
        rows = read_guest_csv(path)

        # assert row before saving
        for row in rows:
            assert len(row) == 2

        User = get_user_model()

        # create users
        for row in rows:
            invite_code = generate_invite_code()
            user = User(username=invite_code)
            user.first_name = row[0]
            user.email = row[1]
            user.password = make_password(invite_code)
            user.save()
