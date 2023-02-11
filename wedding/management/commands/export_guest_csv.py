from django.core.management.base import BaseCommand
import csv

from wedding.models import Guest


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs["path"]
        values = Guest.objects.all().values_list(
            "name",
            "primary_guest__first_name",
            "primary_guest__email",
            "primary_guest__is_rehearsal_guest",
            "primary_guest__username"
        )

        with open(path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in values:
                writer.writerow(row)
