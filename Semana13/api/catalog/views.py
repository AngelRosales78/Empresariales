from django.db.models import ProtectedError
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.exceptions import APIException, ValidationError

from .models import Category, Product
from .permissions import CatalogPermission
from .serializers import CategorySerializer, ProductSerializer


class CategoryInUse(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "No se puede eliminar una categoría que tiene productos."
    default_code = "category_in_use"


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CatalogPermission]
    pagination_class = None  # drop-down lists need every category

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError as error:
            raise CategoryInUse from error


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter("category", int, description="Solo los productos de esta categoría."),
        ]
    )
)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category")  # one query for the nested list
    serializer_class = ProductSerializer
    permission_classes = [CatalogPermission]
    pagination_class = None  # the catalog page shows every product at once

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get("category")
        if self.action == "list" and category:
            if not category.isdecimal():
                raise ValidationError({"category": "Debe ser el identificador de una categoría."})
            queryset = queryset.filter(category_id=int(category))
        return queryset
