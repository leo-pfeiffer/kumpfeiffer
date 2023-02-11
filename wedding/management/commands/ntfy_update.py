from django.core.management.base import BaseCommand
from wedding.utils import notify_with_ntfy, get_status_update_msg


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        ntfy_msg = get_status_update_msg()
        notify_with_ntfy(ntfy_msg)
