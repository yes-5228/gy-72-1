from rest_framework import serializers

from .models import Category, Dish


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "sort_order"]


class DishSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Dish
        fields = [
            "id",
            "category",
            "category_name",
            "name",
            "description",
            "image_url",
            "price",
            "meal_period",
            "available_date",
            "stock",
            "calories",
            "protein",
            "fat",
            "carbohydrate",
            "sodium",
            "allergens",
            "is_recommended",
        ]
