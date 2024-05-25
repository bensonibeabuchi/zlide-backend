from django.contrib import admin
from .models import Testimonial

# Register your models here.

class TestimonialAdmin(admin.ModelAdmin):
    list_display = [ "name", "created_date", "rating"]
    list_filter = ["created_date", "rating"]
    search_fields = ["review"]
    readonly_fields = ["created_date"]

admin.site.register(Testimonial, TestimonialAdmin)