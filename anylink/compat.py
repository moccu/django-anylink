import django


def get_model(app_label, name):
    if django.VERSION < (1, 7):
        from django.db import models
        model = models.get_model(app_label, name)
    else:
        from django.apps import apps
        model = apps.get_registered_model(app_label, name)
    return model
