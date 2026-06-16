from django.contrib import admin

from .models import NutritionProfile


@admin.register(NutritionProfile)
class NutritionProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "calorie_min", "calorie_max", "protein_min", "sodium_max")
