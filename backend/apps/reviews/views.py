from rest_framework import filters, viewsets

from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related("dish__category", "order").all()
    serializer_class = ReviewSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["student_name", "content", "dish__name"]
    ordering_fields = ["created_at", "rating"]

    def get_queryset(self):
        queryset = super().get_queryset()
        dish = self.request.query_params.get("dish")
        if dish:
            queryset = queryset.filter(dish_id=dish)
        return queryset
