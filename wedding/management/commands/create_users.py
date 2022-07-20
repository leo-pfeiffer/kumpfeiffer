import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        name = os.environ.get("DJANGO_SUPERUSER_NAME")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        get_user_model().objects.create_superuser(name, 'admin@myproject.com', password)
