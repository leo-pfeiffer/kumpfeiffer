import logging

from django.core.management.base import BaseCommand

from wedding.utils import read_guest_csv, save_guest_list_rows


logger = logging.getLogger(__name__)


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
        try:
            rows = read_guest_csv(path)
            save_guest_list_rows(rows)
        except Exception as e:
            logger.error(e)
