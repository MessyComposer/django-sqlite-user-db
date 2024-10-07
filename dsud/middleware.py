from contextlib import contextmanager
from asgiref.local import Local

from dsud.utils import set_database_for_user, reset_database_connection


@contextmanager
def load_user_db(user_id):
    try:
        set_database_for_user(user_id)
        yield
    finally:
        reset_database_connection(user_id)

@contextmanager
def request_user_db(user):
    try:
        DatabaseHandlerMiddleware.set_request_user_id(user.id)
        with load_user_db(user.id):
            yield
    finally:
        DatabaseHandlerMiddleware.clear_request_user_id()

class DatabaseHandlerMiddleware:
    _local = Local()

    def __init__(self, get_response):
        self.get_response = get_response

    @classmethod
    def set_request_user_id(cls, user_id):
        cls._local.user_id = user_id
    
    @classmethod
    def clear_request_user_id(cls):
        del cls._local.user_id

    def __call__(self, request):
        if request.user.is_superuser and "admin_user_id" in request.session:
            self.set_request_user_id(request.session["admin_user_id"])
        else:
            self.set_request_user_id(request.user.id)

        with load_user_db(self.get_request_user_id()):
            response = self.get_response(request)
        self.clear_request_user_id()
        return response

    @classmethod
    def get_request_user_id(cls):
        return getattr(cls._local, "user_id", None)
