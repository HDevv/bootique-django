import random
from faker import Faker
from shop.models import Product, Category

faker = Faker()

# créer des catégories et les assigner 
categories = Category.objects.all()

for _ in range(30):
    category = random.choice(categories) if categories.exists() else None
    Product.objects.create(
        title=faker.word(),
        description=faker.text(max_nb_chars=200),
        price=random.randint(10, 100),
        stock=random.randint(1, 20),
        image=f"https://picsum.photos/seed/{random.randint(1, 10000)}/600/400",
        category=category
    )
