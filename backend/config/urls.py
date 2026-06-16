from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.delivery.views import DeliveryTaskViewSet
from apps.menu.views import CategoryViewSet, DishViewSet
from apps.nutrition.views import NutritionAnalysisView
from apps.orders.views import OrderViewSet
from apps.reviews.views import ReviewViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("dishes", DishViewSet)
router.register("orders", OrderViewSet)
router.register("deliveries", DeliveryTaskViewSet)
router.register("reviews", ReviewViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/nutrition/analyze/", NutritionAnalysisView.as_view(), name="nutrition-analyze"),
]
