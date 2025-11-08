from rest_framework import viewsets, permissions, filters
from drf_spectacular.utils import extend_schema, OpenApiExample,
OpenApiParameter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .filters import ProductFilter
@extend_schema(
tags=["Products"],
summary="CRUD Produits",
description=(
"Lister, créer, consulter, modifier et supprimer des produits.\n"
"Pagination (?page=), tri (?ordering=price|-created_at|name),\n"
"filtres: min_price, max_price, category (slug), in_stock=true."
),
parameters=[
created_at, name",
OpenApiParameter(name="ordering", description="ex: price, -
required=False, type=str,
location=OpenApiParameter.QUERY),
OpenApiParameter(name="min_price", description="Prix min (>=)",
required=False, type=float,
location=OpenApiParameter.QUERY),
OpenApiParameter(name="max_price", description="Prix max (<=)",
required=False, type=float,
location=OpenApiParameter.QUERY),
OpenApiParameter(name="category", description="Slug de catégorie",
required=False, type=str,
location=OpenApiParameter.QUERY),
OpenApiParameter(name="in_stock", description="true pour > 0",
required=False, type=bool,
location=OpenApiParameter.QUERY),
],
examples=[
OpenApiExample("Liste filtrée", value="/api/products/?
category=papeterie&min_price=1&in_stock=true"),
],
)
class ProductViewSet(viewsets.ModelViewSet):
queryset = Product.objects.all().order_by("-created_at")
serializer_class = ProductSerializer
permission_classes = [permissions.IsAuthenticatedOrReadOnly]
filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
filterset_class = ProductFilter
ordering_fields = ["created_at", "price", "name"]
ordering = ["-created_at"]
@extend_schema(
tags=["Categories"],
summary="Lister/Créer des catégories",
description="CRUD de catégories; utiliser le slug dans les filtres
produits.",
)
class CategoryViewSet(viewsets.ModelViewSet):
queryset = Category.objects.all().order_by("name")
serializer_class = CategorySerializer
permission_classes = [permissions.IsAuthenticatedOrReadOnly]