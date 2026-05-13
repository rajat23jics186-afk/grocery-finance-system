"""Initialize database with sample data."""

import os
import sys
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.database import SessionLocal, init_db
from backend.models.user import User
from backend.models.product import Product
from backend.models.order import Order, OrderItem
from backend.models.payment import Payment
from backend.auth import hash_password


def init_database():
    """Initialize database with sample data."""
    print("🔄 Creating database tables...")
    init_db()
    print("✓ Database tables created")
    
    db = SessionLocal()
    
    try:
        # Create owner
        print("\n👤 Creating sample users...")
        owner = User(
            username="admin",
            email="admin@grocery.com",
            password_hash=hash_password("admin123"),
            full_name="Store Owner",
            role="owner",
            phone="1234567890",
            city="New York",
            state="NY"
        )
        db.add(owner)
        
        # Create retail customers
        retail_customer = User(
            username="john_retail",
            email="john@example.com",
            password_hash=hash_password("password123"),
            full_name="John Retail",
            role="retail",
            phone="9876543210",
            city="Boston",
            state="MA"
        )
        db.add(retail_customer)
        
        # Create wholesale customer
        wholesale_customer = User(
            username="bulk_buyer",
            email="bulk@example.com",
            password_hash=hash_password("password123"),
            full_name="Bulk Buyer Corp",
            role="wholesale",
            phone="5555555555",
            city="Chicago",
            state="IL",
            credit_limit=50000.0
        )
        db.add(wholesale_customer)
        db.flush()
        print(f"✓ Created {3} sample users")
        
        # Create sample products
        print("\n📦 Creating sample products...")
        products_data = [
            ("Organic Milk", "Dairy", "Fresh organic whole milk", 3.99, 2.99, 50),
            ("Whole Wheat Bread", "Bakery", "Freshly baked whole wheat bread", 4.49, 3.49, 30),
            ("Free Range Eggs", "Dairy", "Dozen free range eggs", 5.99, 4.49, 40),
            ("Cheddar Cheese", "Dairy", "Aged cheddar cheese", 8.99, 6.99, 25),
            ("Fresh Tomatoes", "Produce", "Ripe red tomatoes", 2.99, 1.99, 60),
            ("Broccoli", "Produce", "Fresh green broccoli", 3.49, 2.49, 35),
            ("Chicken Breast", "Meat", "Boneless chicken breast", 9.99, 7.99, 20),
            ("Ground Beef", "Meat", "Lean ground beef", 12.99, 9.99, 15),
            ("Greek Yogurt", "Dairy", "Plain Greek yogurt", 6.99, 5.49, 30),
            ("Whole Grain Pasta", "Pantry", "Organic whole grain pasta", 3.99, 2.99, 45),
        ]
        
        products = []
        for name, category, desc, retail, wholesale, stock in products_data:
            product = Product(
                name=name,
                category=category,
                description=desc,
                retail_price=retail,
                wholesale_price=wholesale,
                quantity_in_stock=stock,
                reorder_level=10,
                supplier="Fresh Foods Co"
            )
            db.add(product)
            products.append(product)
        
        db.flush()
        print(f"✓ Created {len(products)} sample products")
        
        # Create sample orders
        print("\n🛒 Creating sample orders...")
        orders = []
        for i in range(15):
            customer = retail_customer if random.choice([True, False]) else wholesale_customer
            order = Order(
                customer_id=customer.id,
                total_amount=random.uniform(50, 500),
                order_status=random.choice(["pending", "confirmed", "shipped", "delivered"]),
                payment_status=random.choice(["pending", "completed", "partial"]),
                shipping_address=f"{random.randint(100, 999)} Main St",
                order_date=datetime.now() - timedelta(days=random.randint(0, 30))
            )
            db.add(order)
            orders.append(order)
        
        db.flush()
        print(f"✓ Created {len(orders)} sample orders")
        
        # Create order items
        print("\n📋 Creating order line items...")
        for order in orders:
            for _ in range(random.randint(1, 5)):
                product = random.choice(products)
                quantity = random.randint(1, 10)
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=product.retail_price,
                    subtotal=product.retail_price * quantity
                )
                db.add(order_item)
        
        db.commit()
        print(f"✓ Created order line items")
        
        # Create sample payments
        print("\n💳 Creating sample payments...")
        for i, order in enumerate(orders[:10]):
            payment = Payment(
                order_id=order.id,
                customer_id=order.customer_id,
                amount=order.total_amount if order.payment_status == "completed" else order.total_amount * 0.5,
                payment_method=random.choice(["cash", "credit_card", "debit_card", "upi"]),
                transaction_id=f"TXN-{datetime.now().timestamp()}-{i}",
                status="completed"
            )
            db.add(payment)
        
        db.commit()
        print(f"✓ Created sample payments")
        
        print("\n" + "="*50)
        print("✅ Database initialization completed successfully!")
        print("="*50)
        print("\n📝 Sample Credentials:")
        print("  Owner:    admin / admin123")
        print("  Retail:   john_retail / password123")
        print("  Wholesale: bulk_buyer / password123")
        print("\n🚀 Ready to start the server!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
