from django.contrib import admin

from .models import DummyModel, LinkableObject


admin.site.register(LinkableObject)
admin.site.register(DummyModel)
