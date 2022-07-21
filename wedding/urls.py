from django.urls import path

from . import views

urlpatterns = [
    path("", views.SaveTheDateView.as_view(), name="save-the-date"),
    path("login", views.LoginView.as_view(), name="login"),
    path("home", views.HomeView.as_view(), name="home"),
    path("thanks", views.ThanksView.as_view(), name="thanks"),
    path("logout", views.logout_view, name="logout"),
    path("langs", views.LangsView.as_view(), name="langs"),
]
