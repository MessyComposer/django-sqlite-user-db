from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from dsud.db_utils import setup_user_db

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_database(sender, instance, created, **kwargs):
    if not created:
        return
    setup_user_db(instance.id)
