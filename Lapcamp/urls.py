from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("main.urls")),
    path("", include("users.urls")),
    path("", include("groups.urls")),
]

handler404 = "main.views.custom_404"