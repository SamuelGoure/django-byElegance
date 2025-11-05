from rest_framework import viewsets, permissions, filters
from .models import Product
from .serializers import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter


@extend_schema(
    tags=["Products"],
    summary="CRUD Produits",
    description=(
        "Lister, créer, consulter, modifier et supprimer des produits.\n"
        "Supporte pagination (?page=) et tri (?ordering=price, -created_at, name)."
    ),
    examples=[
        OpenApiExample(
            "Exemple de création",
            value={"name": "Pencil", "price": "1.99"},
            request_only=True,
        ),
        OpenApiExample(
            "Exemple de réponse",
            value={"id": 1, "name": "Pencil", "price": "1.99", "created_at": "2025-01-01T12:00:00Z"},
            response_only=True,
        ),
    ],
    parameters=[
        OpenApiParameter(
            name="ordering",
            description="Tri de la liste (ex: price, -created_at, name)",
            required=False,
            type=str,
            location=OpenApiParameter.QUERY,
        ),
    ],
)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]  # à durcir plus tard
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at", "price", "name"]
    ordering = ["-created_at"]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["name", "price"]