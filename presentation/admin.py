from django.contrib import admin
from .models import *


class ZlideAdmin(admin.ModelAdmin):
    list_display = ['custom_display', 'created_at', ]

    def custom_display(self, obj):
        return f"Zlide {obj.id}"  # Custom method to display a formatted string

admin.site.register(Zlide, ZlideAdmin)