from django.db import transaction
from rest_framework import serializers

from apps.menu.models import Dish
from apps.menu.serializers import DishSerializer

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    dish_detail = DishSerializer(source="dish", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "dish", "dish_detail", "quantity", "unit_price"]
        read_only_fields = ["unit_price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "student_name",
            "student_no",
            "phone",
            "delivery_address",
            "pickup_time",
            "note",
            "status",
            "total_amount",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["total_amount", "created_at", "updated_at"]

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("请至少选择一个菜品。")
        for item in value:
            if item["quantity"] < 1:
                raise serializers.ValidationError("菜品数量必须大于 0。")
            if item["dish"].stock < item["quantity"]:
                raise serializers.ValidationError(f"{item['dish'].name} 库存不足。")
        return value

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            dish = Dish.objects.select_for_update().get(id=item_data["dish"].id)
            quantity = item_data["quantity"]
            if dish.stock < quantity:
                raise serializers.ValidationError(f"{dish.name} 库存不足。")
            dish.stock -= quantity
            dish.save(update_fields=["stock"])
            OrderItem.objects.create(order=order, dish=dish, quantity=quantity, unit_price=dish.price)
        order.recalculate_total()
        from apps.delivery.models import DeliveryTask

        DeliveryTask.objects.get_or_create(
            order=order,
            defaults={
                "status": "waiting",
                "estimated_arrival": order.pickup_time,
            },
        )
        return order

    @transaction.atomic
    def update(self, instance, validated_data):
        validated_data.pop("items", None)
        return super().update(instance, validated_data)
