from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('home', views.HomeView.as_view(), name='home'),
    path('thanks', views.ThanksView.as_view(), name='thanks'),
]