from rest_framework import filters, viewsets

from .models import Category, Dish
from .serializers import CategorySerializer, DishSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.select_related("category").all()
    serializer_class = DishSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description", "category__name"]
    ordering_fields = ["available_date", "price", "calories", "stock"]

    def get_queryset(self):
        queryset = super().get_queryset()
        meal_period = self.request.query_params.get("meal_period")
        available_date = self.request.query_params.get("available_date")
        category = self.request.query_params.get("category")
        recommended = self.request.query_params.get("recommended")
        if meal_period:
            queryset = queryset.filter(meal_period=meal_period)
        if available_date:
            queryset = queryset.filter(available_date=available_date)
        if category:
            queryset = queryset.filter(category_id=category)
        if recommended in {"1", "true", "True"}:
            queryset = queryset.filter(is_recommended=True)
        return queryset
