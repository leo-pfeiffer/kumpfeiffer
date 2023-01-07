from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core import serializers

from wedding.dropbox_backup import backup_files
from wedding.models import Rsvp


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        models = [
            {"model": get_user_model(), "name": "users.json"},
            {"model": Rsvp, "name": "rsvp.json"},
        ]

        files_data = []

        for model in models:
            serialized = serializers.serialize("json", model["model"].objects.all())
            files_data.append(
                {"data": serialized.encode("utf-8"), "name": model["name"]}
            )

        backup_files(files_data)
