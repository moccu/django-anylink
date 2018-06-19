from __future__ import unicode_literals
from django.conf.urls import url
from django.contrib import admin

from .views import LinklistView


urlpatterns = [
    url(r'^$', LinklistView.as_view()),
    url(r'^admin/', admin.site.urls),
]
