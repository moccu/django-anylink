from anylink.templatetags.anylink_tags import insert_anylinks
from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
from tinymce.widgets import TinyMCE

from .models import Item, Note, Task


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    model = Item


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }

    list_display = ('subject', 'comment_linked')

    def comment_linked(self, obj):
        return mark_safe(insert_anylinks(obj.comment))


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('colorized_priority', 'description', 'due_to')

    def colorized_priority(self, obj):
        color_mapping = {
            1: 'green',
            2: 'orange',
            3: 'red'
        }
        return mark_safe((
            '<div style="width: 20px; height:100%%; '
            'background-color:{color};">&nbsp;</div>'
        ).format(color=color_mapping[obj.priority]))
