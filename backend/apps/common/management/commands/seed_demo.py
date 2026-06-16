from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.delivery.models import DeliveryTask
from apps.menu.models import Category, Dish
from apps.nutrition.models import NutritionProfile
from apps.orders.models import Order, OrderItem
from apps.reviews.models import Review


class Command(BaseCommand):
    help = "Seed demo data for the school canteen ordering system."

    def handle(self, *args, **options):
        today = timezone.localdate()
        categories = {
            "营养套餐": "主食、荤素、汤品搭配完整。",
            "轻食沙拉": "适合控制热量的学生。",
            "风味小炒": "现炒热菜与地方口味。",
            "汤粥面点": "早餐和晚餐高频选择。",
        }
        category_objs = {}
        for index, (name, description) in enumerate(categories.items(), start=1):
            category_objs[name], _ = Category.objects.update_or_create(
                name=name,
                defaults={"description": description, "sort_order": index},
            )

        dish_rows = [
            ("鸡胸藜麦能量碗", "营养套餐", "lunch", 22.80, 60, 620, 38.5, 18.2, 72.0, 880, "含芝麻", True),
            ("番茄牛腩套餐", "营养套餐", "lunch", 24.50, 50, 760, 34.0, 24.5, 92.0, 1380, "", True),
            ("低脂虾仁沙拉", "轻食沙拉", "dinner", 19.90, 45, 410, 29.5, 11.0, 44.0, 760, "含虾", True),
            ("黑椒牛柳饭", "风味小炒", "dinner", 21.00, 55, 820, 31.0, 27.2, 105.0, 1650, "", False),
            ("青菜香菇鸡丝粥", "汤粥面点", "breakfast", 9.90, 80, 360, 18.0, 7.5, 58.0, 690, "", False),
            ("全麦鸡蛋三明治", "汤粥面点", "breakfast", 12.50, 70, 450, 23.0, 13.0, 56.0, 820, "含蛋、麸质", True),
        ]
        dishes = []
        for name, category, meal, price, stock, calories, protein, fat, carb, sodium, allergens, recommended in dish_rows:
            dish, _ = Dish.objects.update_or_create(
                name=name,
                available_date=today,
                defaults={
                    "category": category_objs[category],
                    "description": f"{name}，适合校园提前订餐与营养搭配。",
                    "image_url": "",
                    "price": price,
                    "meal_period": meal,
                    "stock": stock,
                    "calories": calories,
                    "protein": protein,
                    "fat": fat,
                    "carbohydrate": carb,
                    "sodium": sodium,
                    "allergens": allergens,
                    "is_recommended": recommended,
                },
            )
            dishes.append(dish)

        NutritionProfile.objects.update_or_create(
            name="中学生均衡午餐",
            defaults={
                "calorie_min": 600,
                "calorie_max": 850,
                "protein_min": 25,
                "sodium_max": 1600,
                "note": "适合常规学习日午餐。",
            },
        )

        order, created = Order.objects.get_or_create(
            student_no="S2026001",
            pickup_time=timezone.now() + timedelta(hours=2),
            defaults={
                "student_name": "李同学",
                "phone": "13800000001",
                "delivery_address": "高一教学楼 3 层",
                "note": "少辣",
                "status": "confirmed",
            },
        )
        if created:
            OrderItem.objects.create(order=order, dish=dishes[0], quantity=1, unit_price=dishes[0].price)
            OrderItem.objects.create(order=order, dish=dishes[2], quantity=1, unit_price=dishes[2].price)
            order.recalculate_total()

        DeliveryTask.objects.update_or_create(
            order=order,
            defaults={
                "courier_name": "王师傅",
                "courier_phone": "13900000002",
                "route": "食堂出餐口 -> 高一教学楼",
                "status": "assigned",
                "estimated_arrival": order.pickup_time,
            },
        )

        Review.objects.get_or_create(
            order=order,
            dish=dishes[0],
            student_name="李同学",
            defaults={"rating": 5, "content": "鸡胸肉不柴，藜麦分量足，配送也准时。"},
        )

        self.stdout.write(self.style.SUCCESS("Demo data seeded."))
