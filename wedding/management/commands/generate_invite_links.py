from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import csv

from django.db.models import Q
from django.utils.http import urlencode


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs["path"]
        values = get_user_model().objects.filter(~Q(username="admin"))
        login_url = f"https://kumpfeiffer.wedding/login"

        with open(path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in values:
                invite_url = f"{login_url}?{urlencode({'inviteCode': row.username})}"
                writer.writerow([row.first_name, row.username, invite_url])
