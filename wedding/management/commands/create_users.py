import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        USERS = [
            "leopold",
            "kristina",
            "tina",
            "paul"
        ]
        self.create_users(USERS)

    @staticmethod
    def create_users(users):
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        for user in users:
            get_user_model().objects.create_superuser(
                user, 'admin@myproject.com', password
            )
