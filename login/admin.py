from django.contrib import admin
from . import models

admin.site.register(models.Profile)
admin.site.register(models.Post)
admin.site.register(models.Review)
admin.site.register(models.Comment)

class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','slug')
    prepopulated_fields = {'slug':('name',)}
admin.site.register(models.Category,CategoryAdmin)