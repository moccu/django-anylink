from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from django.contrib import admin

from .views import LinklistView

admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', LinklistView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
)
