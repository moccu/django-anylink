from django.contrib import admin
from .models import Note, Item


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    pass


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass
