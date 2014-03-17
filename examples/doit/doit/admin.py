from django.contrib import admin
from .models import Note, Item, Task


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    pass


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = ('description', 'due_to', 'priority')

    def priority(self, obj):
        color_mapping = {
            1: 'green',
            2: 'orange',
            3: 'red'
        }
        return '<div style="width: 100%%; height:100%%; background-color:{color};">{priority}</div>'.format(
            color=color_mapping[obj.priority],
            priority=obj.priority
        )
    priority.allow_tags = True
