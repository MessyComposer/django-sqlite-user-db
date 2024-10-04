from django.test import TestCase
from django.db import models
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from dsud.db_utils import (
    set_database_for_user,
    delete_user_db,
)

User = get_user_model()


def generate_test_id(field):
    if isinstance(field, models.AutoField):
        return 1338
    elif isinstance(field, models.UUIDField):
        import uuid

        return uuid.uuid4()
    elif isinstance(field, models.CharField):
        return "test_id"
    # Add more field types as needed
    else:
        raise ValueError("Unsupported id field type")


test_user_id = generate_test_id(User._meta.get_field("id"))


class DBUtils(TestCase):
    def test_user_db_unauthorized(self):
        user = AnonymousUser()
        res = set_database_for_user(user.id)
        self.assertEqual(res, None)

    def test_user_db_not_created(self):
        res = set_database_for_user(test_user_id)
        self.assertEqual(res, False)

    def test_user_db_create_delete(self):
        # Create a test user, testing the db management and automatic creation by post_save signal
        self.credentials = {
            "id": test_user_id,
            "username": "testuser",
            "password": "secret",
        }
        user = User.objects.create_user(**self.credentials)

        # Test switching to the user database
        connected = set_database_for_user(user.id)
        self.assertTrue(connected)

        # Test deleting the user database
        res = delete_user_db(user.id)
        self.assertTrue(res)

        # Test deleting the user database again, should return False
        res = delete_user_db(user.id)
        self.assertFalse(res)

    @classmethod
    def tearDownClass(cls):
        delete_user_db(test_user_id)
        super().tearDownClass()
