from importlib import import_module
from django.test.runner import DiscoverRunner
from django.conf import settings
from django.contrib.auth import get_user_model
from dsud.db_utils import delete_user_db

User = get_user_model()


class UserSQLiteDBManagerTestRunner(DiscoverRunner):

    def setup_databases(self, **kwargs):
        old_config = super().setup_databases(**kwargs)
        test_user_details = getattr(
            settings,
            "USER_SQLITE_DB_MANAGER_TEST_USER_DETAILS",
            [
                {"id": 1337, "username": "user_1337", "password": "secret"},
            ],
        )
        for user_details in test_user_details:
            User.objects.create_user(**user_details)
        return old_config

    def teardown_databases(self, old_config, **kwargs) -> None:
        test_user_details = getattr(
            settings,
            "USER_SQLITE_DB_MANAGER_TEST_USER_DETAILS",
            [
                {"id": 1337, "username": "user_1337", "password": "secret"},
            ],
        )
        for user in test_user_details:
            delete_user_db(user["id"])
        return super().teardown_databases(old_config, **kwargs)
