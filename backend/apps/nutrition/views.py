from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import NutritionAnalysisRequestSerializer, NutritionAnalysisSerializer, analyze_dishes


class NutritionAnalysisView(APIView):
    def post(self, request):
        request_serializer = NutritionAnalysisRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        result = analyze_dishes(request_serializer.validated_data["dish_ids"])
        response_serializer = NutritionAnalysisSerializer(result)
        return Response(response_serializer.data)
