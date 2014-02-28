from __future__ import unicode_literals
from django.contrib import admin

from .models import TestModel, LinkableObject


admin.site.register(LinkableObject)
admin.site.register(TestModel)
