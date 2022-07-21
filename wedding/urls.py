from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("save-the-date", views.SaveTheDateView.as_view(), name="save-the-date"),
    path("home", views.HomeView.as_view(), name="home"),
    path("thanks", views.ThanksView.as_view(), name="thanks"),
    path("logout", views.logout_view, name="logout"),
]
