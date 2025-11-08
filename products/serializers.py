from rest_framework import serializers
from .models import Product, Category
class CategorySerializer(serializers.ModelSerializer):
class Meta:
model = Category
fields = ["id", "name", "slug"]
class ProductSerializer(serializers.ModelSerializer):
"""
Représentation d'un produit vendable.
- name: nom commercial
- price: prix TTC en euros (doit être > 0)
- stock: quantité disponible (>= 0)
- category: ID d'une Category (optionnelle)
- created_at: horodatage de création (lecture seule)
"""
category_detail = CategorySerializer(source="category", read_only=True)
class Meta:
model = Product
fields = "__all__"
read_only_fields = ("created_at",)
def validate_price(self, value):
if value <= 0:
return value
raise serializers.ValidationError("Le prix doit être > 0")