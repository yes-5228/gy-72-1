from django.db import models


class NutritionProfile(models.Model):
    name = models.CharField("方案名称", max_length=60, unique=True)
    calorie_min = models.PositiveIntegerField("最低热量")
    calorie_max = models.PositiveIntegerField("最高热量")
    protein_min = models.DecimalField("最低蛋白质", max_digits=6, decimal_places=1)
    sodium_max = models.PositiveIntegerField("最高钠")
    note = models.CharField("提示", max_length=200, blank=True)

    class Meta:
        verbose_name = "营养方案"
        verbose_name_plural = "营养方案"

    def __str__(self):
        return self.name
