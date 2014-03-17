from django.contrib import admin

# class FilmAdmin(admin.ModelAdmin):

#    def film_status(self, obj):
#         if obj.status() != 'active':
#             return '<div style="width:100%%; height:100%%; background-color:orange;">%s</div>' % obj.status()
#         return obj.status()
#     film_status.allow_tags = True

#     list_display = ('id', 'title', 'film_status')

# admin.site.register(Film, FilmAdmin)
