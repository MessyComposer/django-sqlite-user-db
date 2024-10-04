from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", include("dsud.urls", namespace="dsud")),
    path("admin/", admin.site.urls),
]
