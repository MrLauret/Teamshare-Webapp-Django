from django.urls import path
from . import views

urlpatterns = [
    path("", views.blank, name="blank"),
    path("Home", views.home, name="home"),
    path("Join", views.join, name="join"),
    path("Make", views.make, name="make"),
]