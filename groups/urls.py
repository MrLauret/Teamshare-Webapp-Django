from django.urls import path
from .views import *

urlpatterns = [
    path("Group/<int:id>", GroupHome, name="GroupHome"),
    path("Leave/<int:id>", LeaveGroup, name="Leave"),
    path('download/<int:post_id>/', download_post, name='download_post'),
]