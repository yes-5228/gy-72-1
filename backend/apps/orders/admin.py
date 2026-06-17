from django.contrib import admin, messages

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("unit_price",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "student_name", "student_no", "status", "pickup_time", "total_amount", "can_cancel_display")
    list_filter = ("status", "pickup_time")
    search_fields = ("student_name", "student_no", "phone", "delivery_address")
    inlines = [OrderItemInline]
    actions = ["cancel_selected_orders"]

    def can_cancel_display(self, obj):
        can_cancel, reason = obj.can_cancel()
        if can_cancel:
            return "可取消"
        return reason
    can_cancel_display.short_description = "可否取消"

    def cancel_selected_orders(self, request, queryset):
        if not (request.user.is_staff or request.user.is_superuser):
            self.message_user(request, "只有管理员可以批量取消订单。", level=messages.ERROR)
            return
        success_count = 0
        fail_count = 0
        for order in queryset:
            try:
                order.cancel()
                success_count += 1
            except ValueError as e:
                fail_count += 1
                self.message_user(request, f"订单 #{order.id} 取消失败：{e}", level=messages.ERROR)
        if success_count:
            self.message_user(request, f"成功取消 {success_count} 个订单。")
        if fail_count:
            self.message_user(request, f"{fail_count} 个订单取消失败。", level=messages.WARNING)
    cancel_selected_orders.short_description = "取消选中的订单（恢复库存并关闭配送）"
