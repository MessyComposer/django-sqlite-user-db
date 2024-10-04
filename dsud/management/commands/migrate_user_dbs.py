from django.core.management.base import BaseCommand
from django.conf import settings
import os

from dsud.db_utils import setup_user_db


class Command(BaseCommand):
    help = "Migrate all user databases"

    def handle(self, *args, **options):
        for filename in os.listdir(settings.USER_DB_DIR):
            user_id = int(filename.replace("user_", "").replace(".sqlite3", ""))
            setup_user_db(user_id)
