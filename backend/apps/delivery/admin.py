from django.contrib import admin

from .models import DeliveryTask


@admin.register(DeliveryTask)
class DeliveryTaskAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "courier_name", "status", "estimated_arrival", "delivered_at")
    list_filter = ("status", "estimated_arrival")
    search_fields = ("courier_name", "courier_phone", "route", "order__student_name")
