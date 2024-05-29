from django.contrib import admin
from .models import Blog

# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    list_display = ["title", "writer", "date_posted", ]
    list_filter = ["date_posted", "writer"]
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ["title"]
    readonly_fields = ["date_posted"]

admin.site.register(Blog, BlogAdmin)