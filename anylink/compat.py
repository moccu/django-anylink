import django
from django.conf import settings


def get_model(app_label, name):
    if django.VERSION < (1, 7):
        from django.db import models
        model = models.get_model(app_label, name)
    else:
        from django.apps import apps
        model = apps.get_registered_model(app_label, name)
    return model


def is_installed(label):
    # Configure django modeladmin
    if django.VERSION[:2] >= (1, 7):
        from django.apps import apps
        return apps.is_installed(label)
    return label in settings.INSTALLED_APPS


def get_app_module(module_name):
    if django.VERSION[:2] >= (1, 7):
        from django.apps import apps
        return apps.get_app_config(module_name.split('.')[-1]).module
    from django.utils.importlib import import_module
    return import_module(module_name)


def get_all_related_objects(cls):
    if django.VERSION[:2] <= (1, 7):
        # Due to some circumstances, it might happen that the related objects
        # cache is filled before all models are loaded. At this place, we reset
        # the cache if the list is not filled with at least one entry.
        related_objects = cls._meta.get_all_related_objects()

        if len(related_objects) < 1:
            cls._meta._fill_related_objects_cache()
            related_objects = cls._meta.get_all_related_objects()

        return related_objects
    else:
        return [
            f for f in cls._meta.get_fields()
            if f.one_to_many and f.auto_created
        ]


def add_error(form, field, msg, cleaned_data):
    if django.VERSION[:2] <= (1, 6):
        form._errors[field] = form.error_class([msg])
        cleaned_data.pop(field, None)
    else:
        form.add_error(field, msg)
