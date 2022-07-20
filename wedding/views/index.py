from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate


class IndexView(TemplateView):
    template_name = "index.html"

    def get(self, request, **kwargs):
        if "inviteCode" in request.GET:
            inviteCode = request.GET['inviteCode']
            user = authenticate(request, username=inviteCode, password=inviteCode)
            if user is not None:
                login(request, user)
                return redirect('/home')

        return render(request, self.template_name)

    def post(self, request, **kwargs):
        inviteCode = request.POST['invite-code']
        user = authenticate(request, username=inviteCode, password=inviteCode)
        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            return redirect('/')
