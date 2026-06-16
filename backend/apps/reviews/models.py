from django.db import models

from apps.menu.models import Dish
from apps.orders.models import Order


class Review(models.Model):
    order = models.ForeignKey(Order, related_name="reviews", on_delete=models.CASCADE, null=True, blank=True)
    dish = models.ForeignKey(Dish, related_name="reviews", on_delete=models.CASCADE)
    student_name = models.CharField("评价人", max_length=50)
    rating = models.PositiveSmallIntegerField("评分")
    content = models.TextField("评价内容")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "评价"
        verbose_name_plural = "评价"

    def __str__(self):
        return f"{self.dish.name} {self.rating}"
