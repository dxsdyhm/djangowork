from django.contrib import admin

# Register your models here.

from trans import models


@admin.register(models.TransInfo)
class TransInfoAdmin(admin.ModelAdmin):
    list_display = ('zh', 'en')
    list_filter = ('useType',)
