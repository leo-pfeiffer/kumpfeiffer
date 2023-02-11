from django.urls import path

from . import views
from .views.ntfy_update import ntfy_update_view

urlpatterns = [
    path("", views.SaveTheDateView.as_view(), name="save-the-date"),
    path("login", views.LoginView.as_view(), name="login"),
    path("home", views.HomeView.as_view(), name="home"),
    path("thanks", views.ThanksView.as_view(), name="thanks"),
    path("logout", views.logout_view, name="logout"),
    path("ntfy_update", ntfy_update_view, name="ntfy_update"),
]
