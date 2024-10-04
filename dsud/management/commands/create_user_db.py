from django.core.management.base import BaseCommand
from dsud.db_utils import setup_user_db


class Command(BaseCommand):
    help = "Create user database"

    def add_arguments(self, parser):
        parser.add_argument("--user_id", nargs=1, type=int)

    def handle(self, *args, **kwargs):
        user_id = kwargs.get("user_id")[0]
        setup_user_db(user_id)
