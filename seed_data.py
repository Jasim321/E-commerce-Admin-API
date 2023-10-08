from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Product, Category, Sale, Inventory
from datetime import datetime, timedelta
import random


def create_demo_data():
    db: Session = SessionLocal()

    categories = ["Electronics", "Books", "Clothing", "Toys"]
    for cat in categories:
        category = Category(name=cat)
        db.add(category)

    db.commit()

    products = [
        Product(name="Ice Maker", description="E-book reader", price=89.99, category_id=1),
        Product(name="Walmart Basic T-Shirt", description="Cotton T-shirt", price=9.99, category_id=3),
        Product(name="Coffee beater", description="Premium Coffee beater", price=5.99, category_id=3),
    ]
    for product in products:
        db.add(product)

    db.commit()

    today = datetime.today()
    for product in products:
        for _ in range(10):
            sale_date = today - timedelta(days=random.randint(0, 30))
            sale = Sale(product_id=product.id, sale_date=sale_date, sale_quantity=random.randint(1, 5))
            db.add(sale)

    db.commit()

    for product in products:
        inventory = Inventory(product_id=product.id, quantity=random.randint(10, 100), created_at=today)
        db.add(inventory)

    db.commit()

    print("Demo data created successfully!")
    db.close()


if __name__ == "__main__":
    create_demo_data()
