from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from django.contrib import admin

from .views import LinklistView

import django

if django.VERSION[:2] < (1, 7):
    admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', LinklistView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
)
