from django.apps import apps
from dsud.middleware import DatabaseSwitchMiddleware


class UserSpecificDatabaseRouter:

    def check_user_specific(self, model):
        return getattr(model, "_is_user_model", False)

    def db_for_read(self, model, **hints):
        if self.check_user_specific(model):
            user_id = DatabaseSwitchMiddleware.get_request_user_id()
            return f"user_{user_id}"
        return "default"

    def db_for_write(self, model, **hints):
        if self.check_user_specific(model):
            user_id = DatabaseSwitchMiddleware.get_request_user_id()
            return f"user_{user_id}"
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        return self.check_user_specific(obj1) == self.check_user_specific(obj2)

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name is None:
            app_config = apps.get_app_config(app_label)
            if db != "default":
                return getattr(app_config, "_is_user_specific", False)
            return not getattr(app_config, "_is_user_specific", False)

        model = apps.get_model(app_label, model_name)
        if db != "default":
            return self.check_user_specific(model)
        return not self.check_user_specific(model)
