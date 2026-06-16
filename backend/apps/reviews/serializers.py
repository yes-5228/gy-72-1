from rest_framework import serializers

from apps.menu.serializers import DishSerializer

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    dish_detail = DishSerializer(source="dish", read_only=True)

    class Meta:
        model = Review
        fields = ["id", "order", "dish", "dish_detail", "student_name", "rating", "content", "created_at"]
        read_only_fields = ["created_at"]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("评分必须在 1 到 5 之间。")
        return value
