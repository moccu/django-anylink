from django.contrib import admin

from .models import Link, LinkableObject, Linklist


class LinkInline(admin.TabularInline):
    model = Link
    extra = 0
    raw_id_fields = ('link',)


class LinklistAdmin(admin.ModelAdmin):
    inlines = (LinkInline,)

admin.site.register(Linklist, LinklistAdmin)

admin.site.register(LinkableObject)
