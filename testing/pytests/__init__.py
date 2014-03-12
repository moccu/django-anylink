from __future__ import unicode_literals
import django


if django.VERSION[:2] < (1, 7):
    from django.contrib import admin
    # We need to admin.autodiscover here because pytest won't load the urls file
    # and therefore won't register the apps.
    admin.autodiscover()
else:
    django.setup()
