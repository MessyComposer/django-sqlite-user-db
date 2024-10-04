from django.contrib import admin
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.urls import reverse

User = get_user_model()


def set_user(request):
    if not request.user.is_superuser:
        del request.session["admin_user_id"]
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    if "user_id" in request.GET:
        request.session["admin_user_id"] = request.GET["user_id"]
        request.session.modified = True
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def unset_user(request):
    if not request.user.is_superuser:
        del request.session["admin_user_id"]
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    if "admin_user_id" in request.session:
        del request.session["admin_user_id"]
        request.session.modified = True
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
        "switch_user_button",
    )

    def switch_user_button(self, obj):
        url = reverse("dsud:set_user") + f"?user_id={obj.id}"
        return format_html(
            '<a class="button" href="{}">Switch User</a>',
            url,
        )
