from django.urls import path
from dsud.admin import set_user, unset_user

app_name = "dsud"
urlpatterns = [
    path("set_user/", set_user, name="set_user"),
    path("unset_user/", unset_user, name="unset_user"),
]
