from django.contrib import admin

from django.urls import include, re_path


urlpatterns = [
    url(r'', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),
]
