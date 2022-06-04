import os

from django.core.management.base import BaseCommand

from wedding.models import Guest
from wedding.utils import read_guest_csv


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
        for row in rows:
            Guest.objects.create(name=row[0], email=row[1])
