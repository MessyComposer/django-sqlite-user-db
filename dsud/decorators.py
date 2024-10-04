from django.apps import apps
from django.db.models.fields.related import ManyToManyField


def _mark_user_model(model, is_user_model):
    model._is_user_model = is_user_model
    # Handle ManyToManyField intermediate tables
    for field in model._meta.get_fields():
        if isinstance(field, ManyToManyField):
            field.remote_field.through._is_user_model = is_user_model


def user_model(cls):
    _mark_user_model(cls, True)
    return cls


def public_model(cls):
    _mark_user_model(cls, False)
    return cls


def user_specific_app_config(cls):
    original_ready = cls.ready

    def ready(self):
        self._is_user_specific = True
        for model in self.get_models():
            if hasattr(model, "_is_user_model"):
                continue
            _mark_user_model(model, True)
        original_ready(self)

    cls.ready = ready
    return cls
