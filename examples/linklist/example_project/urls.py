from django.urls import re_path
from django.contrib import admin

from .views import LinklistView


urlpatterns = [
    re_path(r'^$', LinklistView.as_view()),
    re_path(r'^admin/', admin.site.urls),
]
