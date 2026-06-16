from rest_framework import serializers

from apps.orders.serializers import OrderSerializer

from .models import DeliveryTask


class DeliveryTaskSerializer(serializers.ModelSerializer):
    order_detail = OrderSerializer(source="order", read_only=True)
    is_locked = serializers.SerializerMethodField()
    lock_reason = serializers.SerializerMethodField()

    class Meta:
        model = DeliveryTask
        fields = [
            "id",
            "order",
            "order_detail",
            "courier_name",
            "courier_phone",
            "route",
            "status",
            "is_locked",
            "lock_reason",
            "estimated_arrival",
            "delivered_at",
            "updated_at",
        ]
        read_only_fields = ["is_locked", "lock_reason"]

    def get_is_locked(self, obj):
        return obj.is_locked_by_cancellation()

    def get_lock_reason(self, obj):
        if obj.is_locked_by_cancellation():
            return "该订单已取消，配送任务已关闭"
        return None

    def validate_status(self, value):
        instance = self.instance
        if instance is not None:
            can_change, message = instance.can_change_status_to(value)
            if not can_change:
                raise serializers.ValidationError(message)
        return value
