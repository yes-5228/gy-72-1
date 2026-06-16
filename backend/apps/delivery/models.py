from django.db import models

from apps.orders.models import Order


class DeliveryTask(models.Model):
    STATUS_CHOICES = [
        ("waiting", "待分配"),
        ("assigned", "已分配"),
        ("picked", "已取餐"),
        ("delivered", "已送达"),
        ("failed", "异常"),
    ]

    order = models.OneToOneField(Order, related_name="delivery", on_delete=models.CASCADE)
    courier_name = models.CharField("配送员", max_length=50, blank=True)
    courier_phone = models.CharField("配送电话", max_length=30, blank=True)
    route = models.CharField("配送路线", max_length=160, blank=True)
    status = models.CharField("配送状态", max_length=20, choices=STATUS_CHOICES, default="waiting")
    estimated_arrival = models.DateTimeField("预计送达", null=True, blank=True)
    delivered_at = models.DateTimeField("实际送达", null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["status", "estimated_arrival"]
        verbose_name = "配送任务"
        verbose_name_plural = "配送任务"

    def __str__(self):
        return f"配送任务 #{self.order_id}"
