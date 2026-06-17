from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import Order
from .serializers import OrderCancelSerializer, OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items__dish__category").all()
    serializer_class = OrderSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["student_name", "student_no", "phone", "delivery_address"]
    ordering_fields = ["created_at", "pickup_time", "total_amount"]

    def get_queryset(self):
        queryset = super().get_queryset()
        status_value = self.request.query_params.get("status")
        if status_value:
            queryset = queryset.filter(status=status_value)
        student_no = self.request.query_params.get("student_no")
        if student_no:
            queryset = queryset.filter(student_no=student_no)
        return queryset

    @staticmethod
    def _check_cancel_permission(request, order):
        user = request.user
        if user and (user.is_staff or user.is_superuser):
            return True
        operator_student_no = request.data.get("operator_student_no") or request.query_params.get("operator_student_no")
        if operator_student_no and operator_student_no.strip() == order.student_no.strip():
            return True
        return False

    @action(detail=True, methods=["post"], serializer_class=OrderCancelSerializer)
    def cancel(self, request, pk=None):
        order = self.get_object()

        if not self._check_cancel_permission(request, order):
            raise PermissionDenied("只有订单本人或管理员可以取消该订单")

        serializer = self.get_serializer(data=request.data, context={"order": order})
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"status": "cancelled", "message": "订单已取消，库存已恢复，配送任务已关闭"},
            status=status.HTTP_200_OK,
        )
