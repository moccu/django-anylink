from django.contrib import admin


# We need to admin.autodiscover here because pytest won't load the urls file
# and therefore won't register the apps.
admin.autodiscover()
