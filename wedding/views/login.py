import logging

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate

logger = logging.getLogger(__name__)


class LoginView(TemplateView):
    template_name = "login.html"

    def get(self, request, **kwargs):
        if "inviteCode" in request.GET:
            invite_code = request.GET["inviteCode"]
            user = authenticate(request, username=invite_code, password=invite_code)
            if user is not None:
                login(request, user)
                logger.info(f"Successful login of user {user}")
                return redirect("/home")

        return render(request, self.template_name)

    def post(self, request, **kwargs):
        if "invite-code" not in request.POST:
            return redirect("/")

        invite_code = request.POST["invite-code"]
        user = authenticate(request, username=invite_code, password=invite_code)

        if user is not None:
            login(request, user)
            logger.info(f"Successful login of user {user}")
            return redirect("/home")

        return redirect("/")
