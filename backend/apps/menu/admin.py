from django.contrib import admin

from .models import Category, Dish


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "sort_order", "description")
    search_fields = ("name",)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "meal_period", "available_date", "price", "stock", "is_recommended")
    list_filter = ("meal_period", "available_date", "category", "is_recommended")
    search_fields = ("name", "description")
