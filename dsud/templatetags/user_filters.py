from django import template
from django.contrib.auth import get_user_model

register = template.Library()

User = get_user_model()


@register.filter(name="user_id_to_username")
def user_id_to_username(user_id):
    try:
        user = User.objects.get(id=user_id)
        return user.username
    except User.DoesNotExist:
        return "Unknown User"
