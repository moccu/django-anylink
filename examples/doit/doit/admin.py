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

    list_display = ('colorized_priority', 'description', 'due_to')

    def colorized_priority(self, obj):
        color_mapping = {
            1: 'green',
            2: 'orange',
            3: 'red'
        }
        return '<div style="width: 20px; height:100%%; background-color:{color};">&nbsp;</div>'.format(
            color=color_mapping[obj.priority],
        )
    colorized_priority.allow_tags = True
