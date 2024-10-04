from contextlib import contextmanager

from dsud.middleware import DatabaseSwitchMiddleware, switch_database_for_user


@contextmanager
def set_user_in_middleware(user):
    print("Set user in middleware", user.id)
    try:
        DatabaseSwitchMiddleware._local.user_id = user.id
        with switch_database_for_user(user.id):
            yield
    finally:
        del DatabaseSwitchMiddleware._local.user_id
