from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("dish", "student_name", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("student_name", "content", "dish__name")
