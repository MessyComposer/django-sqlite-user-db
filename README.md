# Django SQLite User DB (DSUD)
[![codecov](https://codecov.io/gh/MessyComposer/django-sqlite-user-db/graph/badge.svg?token=2ER3QRHUT0)](https://codecov.io/gh/MessyComposer/django-sqlite-user-db)

**Disclaimer:**  
This package is purely experimental and is not intended for production use. Use at your own discretion.

---

## Overview

Django SQLite User DB (DSUD) is a Django package that allows each user to have their own individual SQLite database. This enables user-specific data management while maintaining a lightweight and simple setup. Perfect for development, prototyping, and learning, DSUD provides a unique approach to user data storage.

## Features

- Individual SQLite databases for each user
- Easy integration with existing Django projects
- Lightweight and minimal configuration

## Installation

To install DSUD, do the following modifications in your Django settings:

```python
INSTALLED_APPS = [
    ...
    'dsud',
    ...
]
MIDDLEWARE = [
    ...
    "dsud.middleware.DatabaseSwitchMiddleware",
    ...
]
DATABASE_ROUTERS = ["dsud.router.UserSpecificDatabaseRouter"]
TEST_RUNNER = "dsud.test_runner.UserSQLiteDBManagerTestRunner"
```

## Defining Users For Test Cases

In your settings, you can define test users by adding setting `USER_SQLITE_DB_MANAGER_TEST_USER_DETAILS`. This setting should contain a list of user payloads, such as:

```python
USER_SQLITE_DB_MANAGER_TEST_USER_DETAILS = [
    {"id": 1337, "username": "user_1337", "password": "secret"},
    # Add more test users as needed
]
```

These users will be enrolled during the test runner's `setup_database` step, including the creation of their individual databases. They will also be automatically torn down after the tests are completed.


## Admin Panel Integration
This assumes you've registered `dsud.admin.UserAdmin` for your User model, or inherit from it in a custom model admin and include `"switch_user_button"` in `list_display`.

To easily manage user databases through the Django admin panel, follow these steps:

1. **Update `urls.py`**:

    Add the following path to your base `urls.py` file:

    ```python
    from django.urls import path, include

    urlpatterns = [
         path(
              "admin/",
              include(
                    "dsud.urls",
                    namespace="dsud",
              ),
         ),
         ...
    ]
    ```

2. **Customize Admin Templates**:


    Create a file at `templates/admin/base_site.html` with the following contents:

    ```html
    {% extends "dsud/base_site.html" %}
    ```

This will allow you to manage user-specific databases directly from the Django admin interface.
Simply go to the users table, and click the "Switch user" button



## Manual Database Entry

If you need to  create entries in the user-specific database outside of requests (like test case setups for example), you can use the `set_user_in_middleware` context manager provided by DSUD. Here is an example:

```python
from dsud.context_manager import set_user_in_middleware
from your_app.models import Model

# Assuming you have a user instance
user = User.objects.get(username='example_user')

# Manually create entries in the user's database
with set_user_in_middleware(user):
    obj1 = Model.objects.create(...)
    obj2 = Model.objects.create(...)

```

This approach allows you to explicitly set the user context and perform database operations within that context, ensuring that the entries are created in the correct user-specific database.

---

Feel free to customize further based on your project's specific details!