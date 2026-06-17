import uuid

from django.db import models, transaction

from apps.menu.models import Dish


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "待确认"),
        ("confirmed", "已确认"),
        ("preparing", "备餐中"),
        ("delivering", "配送中"),
        ("completed", "已完成"),
        ("cancelled", "已取消"),
    ]

    CANCELLABLE_STATUSES = {"pending", "confirmed"}

    student_name = models.CharField("学生姓名", max_length=50)
    student_no = models.CharField("学号", max_length=30)
    phone = models.CharField("联系电话", max_length=30)
    delivery_address = models.CharField("配送地址", max_length=160)
    pickup_time = models.DateTimeField("预约送达时间")
    note = models.CharField("备注", max_length=200, blank=True)
    status = models.CharField("状态", max_length=20, choices=STATUS_CHOICES, default="pending")
    total_amount = models.DecimalField("总金额", max_digits=9, decimal_places=2, default=0)
    cancel_token = models.UUIDField("取消令牌", default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "订单"
        verbose_name_plural = "订单"

    def __str__(self):
        return f"{self.student_name} {self.created_at:%Y%m%d%H%M}"

    def recalculate_total(self):
        total = sum(item.quantity * item.unit_price for item in self.items.all())
        self.total_amount = total
        self.save(update_fields=["total_amount", "updated_at"])

    def can_cancel(self):
        if self.status == "cancelled":
            return False, "订单已取消"
        if self.status not in self.CANCELLABLE_STATUSES:
            return False, "订单已进入备餐或配送流程，无法取消"
        if hasattr(self, "delivery") and self.delivery:
            delivery = self.delivery
            if delivery.status in {"picked", "delivered"}:
                return False, "订单已取餐或已送达，无法取消"
        return True, "可以取消"

    @transaction.atomic
    def cancel(self):
        can_cancel, message = self.can_cancel()
        if not can_cancel:
            raise ValueError(message)

        for item in self.items.select_related("dish").all():
            dish = Dish.objects.select_for_update().get(id=item.dish.id)
            dish.stock += item.quantity
            dish.save(update_fields=["stock"])

        if hasattr(self, "delivery") and self.delivery:
            self.delivery.status = "failed"
            self.delivery.save(update_fields=["status", "updated_at"])

        self.status = "cancelled"
        self.save(update_fields=["status", "updated_at"])

        return True


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, related_name="order_items", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField("数量", default=1)
    unit_price = models.DecimalField("单价", max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = "订单明细"
        verbose_name_plural = "订单明细"

    def __str__(self):
        return f"{self.dish.name} x {self.quantity}"
