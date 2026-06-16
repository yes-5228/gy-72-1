from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("unit_price",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "student_name", "student_no", "status", "pickup_time", "total_amount")
    list_filter = ("status", "pickup_time")
    search_fields = ("student_name", "student_no", "phone", "delivery_address")
    inlines = [OrderItemInline]
