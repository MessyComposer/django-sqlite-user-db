from contextlib import contextmanager
from asgiref.local import Local

from dsud.db_utils import set_database_for_user, reset_database_connection


@contextmanager
def switch_database_for_user(user_id):
    try:
        set_database_for_user(user_id)
        yield
    finally:
        reset_database_connection(user_id)


class DatabaseSwitchMiddleware:
    _local = Local()

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_superuser and "admin_user_id" in request.session:
            self._local.user_id = request.session["admin_user_id"]
        else:
            self._local.user_id = request.user.id

        # Identify user and set database
        with switch_database_for_user(self._local.user_id):
            response = self.get_response(request)
        del self._local.user_id
        return response

    @classmethod
    def get_request_user_id(cls):
        return getattr(cls._local, "user_id", None)
