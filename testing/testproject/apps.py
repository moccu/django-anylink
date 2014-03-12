# Django 1.7 compatibility. This file won't be loaded for Django < 1.7
from django.apps import AppConfig


class TestprojectConfig(AppConfig):
    name = 'testproject'
    verbose_name = "Test Project"
