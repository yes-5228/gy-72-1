from django.db import models


class Category(models.Model):
    name = models.CharField("分类名称", max_length=40, unique=True)
    description = models.CharField("说明", max_length=160, blank=True)
    sort_order = models.PositiveIntegerField("排序", default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name = "菜品分类"
        verbose_name_plural = "菜品分类"

    def __str__(self):
        return self.name


class Dish(models.Model):
    MEAL_CHOICES = [
        ("breakfast", "早餐"),
        ("lunch", "午餐"),
        ("dinner", "晚餐"),
    ]

    category = models.ForeignKey(Category, related_name="dishes", on_delete=models.PROTECT)
    name = models.CharField("菜品名称", max_length=80)
    description = models.TextField("菜品介绍", blank=True)
    image_url = models.URLField("图片地址", blank=True)
    price = models.DecimalField("价格", max_digits=8, decimal_places=2)
    meal_period = models.CharField("供餐时段", max_length=20, choices=MEAL_CHOICES)
    available_date = models.DateField("供应日期")
    stock = models.PositiveIntegerField("库存", default=0)
    calories = models.PositiveIntegerField("热量(kcal)", default=0)
    protein = models.DecimalField("蛋白质(g)", max_digits=6, decimal_places=1, default=0)
    fat = models.DecimalField("脂肪(g)", max_digits=6, decimal_places=1, default=0)
    carbohydrate = models.DecimalField("碳水(g)", max_digits=6, decimal_places=1, default=0)
    sodium = models.PositiveIntegerField("钠(mg)", default=0)
    allergens = models.CharField("过敏原", max_length=160, blank=True)
    is_recommended = models.BooleanField("推荐", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["available_date", "meal_period", "category__sort_order", "name"]
        verbose_name = "菜品"
        verbose_name_plural = "菜品"

    def __str__(self):
        return self.name
