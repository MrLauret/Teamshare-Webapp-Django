from django.urls import path
from .views import *

urlpatterns = [
    path("Login", login, name="login"),
    path("Register", register, name="register"),
    path("Logout", logout, name="logout"),
]