import logging

from django.contrib.auth import logout
from django.shortcuts import redirect


logger = logging.getLogger(__name__)


def logout_view(request):
    logger.info(f"Logging out user {request.user}")
    logout(request)
    return redirect("/home")
