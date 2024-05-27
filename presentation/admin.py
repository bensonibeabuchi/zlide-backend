from django.contrib import admin
from .models import *


class ZlideAdmin(admin.ModelAdmin):
    list_display = ['presentation_name', 'created_at', ]
    list_filter = ['presentation_name']

admin.site.register(Zlide, ZlideAdmin)