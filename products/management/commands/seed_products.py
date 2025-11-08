from django.core.management.base import BaseCommand
from products.models import Product, Category

class Command(BaseCommand):
    help = "Seed demo categories and products safely"

    def handle(self, *args, **kwargs):
        # --- Catégories ---
        cats = [
            ("Papeterie", "papeterie"),
            ("Informatique", "informatique"),
        ]
        obj = {}
        for name, slug in cats:
            category = Category.objects.filter(name=name).first()
            if not category:
                category = Category.objects.create(name=name, slug=slug)
            obj[slug] = category

        # --- Produits ---
        data = [
            {"name": "Crayon", "price": 1.50, "stock": 10, "category": obj["papeterie"]},
            {"name": "Cahier", "price": 3.20, "stock": 5, "category": obj["papeterie"]},
            {"name": "Souris", "price": 12.90, "stock": 2, "category": obj["informatique"]},
        ]

        for d in data:
            Product.objects.update_or_create(
                name=d["name"],
                category=d["category"],
                defaults={
                    "price": d["price"],
                    "stock": d["stock"],
                }
            )

        self.stdout.write(self.style.SUCCESS("Seeded demo categories and products safely!"))
