from django.core.management import call_command
from django.db import connections
from django.conf import settings
import os


def get_user_database_alias(user_id):
    return f"user_{user_id}"


def get_user_database_path(user_id):
    # Using in-memory database for testing doesn't work too nicely, tackle this later
    # if settings.TEST:
    #     return ":memory:"
    db_name = f"{get_user_database_alias(user_id)}.sqlite3"
    return os.path.join(settings.USER_DB_DIR, db_name)


def set_database_for_user(user_id):
    """
    Dynamically sets the database for the current user.
    Assumes user-specific databases are named using the pattern 'user_{user_id}.sqlite3'
    and are stored in a 'db' directory within the Django project's base directory.
    """
    if not user_id:
        return None
    
    # Construct the path to the user-specific database
    db_path = get_user_database_path(user_id)

    # Check if the database file exists; if not, you might want to create it or handle as an error
    if not os.path.exists(db_path):
        # Log an error or handle accordingly
        print(f"Database for user {db_path} does not exist.")
        return False

    user_db_alias = get_user_database_alias(user_id)
    connections.databases[user_db_alias] = connections.databases["default"].copy()
    connections.databases[user_db_alias]["NAME"] = db_path
    connections[user_db_alias].ensure_connection()
    return True


def reset_database_connection(user_id):
    """
    Closes and removes the user-specific database connection.
    """
    user_db_alias = get_user_database_alias(user_id)
    # print("Reset database connection", user_db_alias, connections)
    if user_db_alias in connections:
        connections[user_db_alias].close()
        del connections[user_db_alias]
    if user_db_alias in settings.DATABASES:
        del settings.DATABASES[user_db_alias]


def setup_user_db(user_id):
    db_path = get_user_database_path(user_id)

    try:
        # Apply migrations to the user database
        user_db_alias = get_user_database_alias(user_id)
        connections.databases[user_db_alias] = connections.databases["default"].copy()
        connections.databases[user_db_alias]["NAME"] = db_path
        call_command("migrate", database=user_db_alias, interactive=False)
        return True
    except Exception as e:  # pragma: no cover
        print(f"Error migrating database {db_path}: {e}")
        return False
    finally:
        reset_database_connection(user_id)


def delete_user_db(user_id):
    db_path = get_user_database_path(user_id)

    if os.path.exists(db_path):
        reset_database_connection(user_id)
        os.remove(db_path)
        return True
    return False
