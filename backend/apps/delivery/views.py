from rest_framework import filters, viewsets

from .models import DeliveryTask
from .serializers import DeliveryTaskSerializer


class DeliveryTaskViewSet(viewsets.ModelViewSet):
    queryset = DeliveryTask.objects.select_related("order").prefetch_related("order__items__dish__category").all()
    serializer_class = DeliveryTaskSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["courier_name", "courier_phone", "route", "order__student_name"]
    ordering_fields = ["estimated_arrival", "updated_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        status_value = self.request.query_params.get("status")
        if status_value:
            queryset = queryset.filter(status=status_value)
        return queryset
