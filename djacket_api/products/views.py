from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProductViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):

    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Product.objects.select_related("category")
        category_id = self.request.query_params.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    @action(detail=False, methods=["get"], url_path="latest")
    def latest(self, request):
        latest_products = self.get_queryset().order_by("-created_at")[:4]
        serializer = self.get_serializer(latest_products, many=True)
        return Response(serializer.data)
