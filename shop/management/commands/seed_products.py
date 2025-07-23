from django.core.management.base import BaseCommand
from faker import Faker
import random
from shop.models import Product, Category

# SCRIPT DE GENERATION D'IMG ALEATOIRES

fake = Faker()

class Command(BaseCommand):
    help = "Génère des produits de test"

    def handle(self, *args, **kwargs):
        categories = list(Category.objects.all())
        if not categories:
            self.stdout.write(self.style.WARNING("Veuillez créer des catégories d'abord."))
            return

        for _ in range(30):
            produit = Product.objects.create(
                title=fake.sentence(nb_words=3),
                description=fake.text(),
                price=round(random.uniform(10, 300), 2),
                category=random.choice(categories),
                image="products/default.jpg"  # image factice
            )
            self.stdout.write(self.style.SUCCESS(f"Produit créé : {produit.title}"))
