"""
Script to seed the database with dummy data
Run this script after creating the database tables:
    python seed_data.py
"""

import logging
from datetime import datetime, timedelta
from app.core.database import SessionLocal, engine, Base
from app.models import Medicine, Sales, PurchaseOrder

# Suppress SQLAlchemy logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()


def seed_medicines():
    """Create 10 dummy medicines"""
    medicines_data = [
        Medicine(
            name="Paracetamol 500mg",
            description="Pain reliever and fever reducer",
            price=5.99,
            stock_quantity=150,
            reorder_level=50,
            category="Pain Relief",
            manufacturer="Pharma Labs",
            expiry_date=datetime.utcnow() + timedelta(days=365),
            is_active=1
        ),
        Medicine(
            name="Ibuprofen 200mg",
            description="Anti-inflammatory pain reliever",
            price=7.99,
            stock_quantity=30,  # Low stock
            reorder_level=50,
            category="Pain Relief",
            manufacturer="HealthCare Inc",
            expiry_date=datetime.utcnow() + timedelta(days=365),
            is_active=1
        ),
        Medicine(
            name="Amoxicillin 500mg",
            description="Antibiotic for bacterial infections",
            price=15.99,
            stock_quantity=100,
            reorder_level=40,
            category="Antibiotics",
            manufacturer="MediTech Corp",
            expiry_date=datetime.utcnow() + timedelta(days=365),
            is_active=1
        ),
        Medicine(
            name="Metformin 500mg",
            description="Medicine for type 2 diabetes",
            price=12.99,
            stock_quantity=200,
            reorder_level=80,
            category="Diabetes",
            manufacturer="Pharma Labs",
            expiry_date=datetime.utcnow() + timedelta(days=365),
            is_active=1
        ),
        Medicine(
            name="Lisinopril 10mg",
            description="Blood pressure medication",
            price=9.99,
            stock_quantity=120,
            reorder_level=60,
            category="Cardiovascular",
            manufacturer="CardioPharm",
            expiry_date=datetime.utcnow() + timedelta(days=365),
            is_active=1
        ),
        Medicine(
            name="Atorvastatin 20mg",
            description="Cholesterol lowering medication",
            price=18.99,
            stock_quantity=20,  # Low stock
            reorder_level=50,
            category="Cardiovascular",
            manufacturer="CardioPharm",
            expiry_date=datetime.utcnow() + timedelta(days=365),
            is_active=1
        ),
        Medicine(
            name="Vitamin D3 1000IU",
            description="Vitamin supplement for bone health",
            price=8.99,
            stock_quantity=250,
            reorder_level=100,
            category="Supplements",
            manufacturer="NutriCare",
            expiry_date=datetime.utcnow() + timedelta(days=365),
            is_active=1
        ),
        Medicine(
            name="Levothyroxine 50mcg",
            description="Thyroid hormone replacement",
            price=11.99,
            stock_quantity=180,
            reorder_level=70,
            category="Endocrine",
            manufacturer="ThyroMed",
            expiry_date=datetime.utcnow() + timedelta(days=365),
            is_active=1
        ),
        Medicine(
            name="Cetirizine 10mg",
            description="Antihistamine for allergies",
            price=6.99,
            stock_quantity=45,  # Low stock
            reorder_level=50,
            category="Allergy",
            manufacturer="AllergyFree Inc",
            expiry_date=datetime.utcnow() + timedelta(days=365),
            is_active=1
        ),
        Medicine(
            name="Omeprazole 20mg",
            description="Proton pump inhibitor for acid reflux",
            price=10.99,
            stock_quantity=160,
            reorder_level=60,
            category="Gastro",
            manufacturer="GastroMed",
            expiry_date=datetime.utcnow() + timedelta(days=365),
            is_active=1
        ),
    ]
    
    db.add_all(medicines_data)
    db.commit()
    print(f"✓ Added {len(medicines_data)} medicines")
    return medicines_data


def seed_sales(medicines):
    """Create sample sales for today"""
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    sales_data = [
        Sales(
            medicine_id=medicines[0].id,
            quantity_sold=5,
            sale_price=5.99,
            sale_date=today_start + timedelta(hours=8)
        ),
        Sales(
            medicine_id=medicines[1].id,
            quantity_sold=3,
            sale_price=7.99,
            sale_date=today_start + timedelta(hours=9)
        ),
        Sales(
            medicine_id=medicines[2].id,
            quantity_sold=2,
            sale_price=15.99,
            sale_date=today_start + timedelta(hours=10)
        ),
        Sales(
            medicine_id=medicines[3].id,
            quantity_sold=4,
            sale_price=12.99,
            sale_date=today_start + timedelta(hours=11)
        ),
        Sales(
            medicine_id=medicines[4].id,
            quantity_sold=6,
            sale_price=9.99,
            sale_date=today_start + timedelta(hours=12)
        ),
    ]
    
    db.add_all(sales_data)
    db.commit()
    print(f"✓ Added {len(sales_data)} sales records for today")


def seed_purchase_orders(medicines):
    """Create sample purchase orders"""
    purchase_orders_data = [
        PurchaseOrder(
            medicine_id=medicines[1].id,  # Ibuprofen - low stock
            quantity_ordered=100,
            order_date=datetime.utcnow() - timedelta(days=2),
            expected_delivery_date=datetime.utcnow() + timedelta(days=3),
            status="pending"
        ),
        PurchaseOrder(
            medicine_id=medicines[5].id,  # Atorvastatin - low stock
            quantity_ordered=150,
            order_date=datetime.utcnow() - timedelta(days=1),
            expected_delivery_date=datetime.utcnow() + timedelta(days=5),
            status="pending"
        ),
        PurchaseOrder(
            medicine_id=medicines[8].id,  # Cetirizine - low stock
            quantity_ordered=200,
            order_date=datetime.utcnow() - timedelta(days=5),
            expected_delivery_date=datetime.utcnow() - timedelta(days=2),
            status="delivered"
        ),
        PurchaseOrder(
            medicine_id=medicines[0].id,  # Paracetamol
            quantity_ordered=300,
            order_date=datetime.utcnow() - timedelta(days=10),
            expected_delivery_date=datetime.utcnow() - timedelta(days=8),
            status="delivered"
        ),
    ]
    
    db.add_all(purchase_orders_data)
    db.commit()
    print(f"✓ Added {len(purchase_orders_data)} purchase orders")


def main():
    """Run all seed functions"""
    try:
        print("\n🌱 Starting database seeding...\n")
        
        # Check if data already exists
        existing_count = db.query(Medicine).count()
        if existing_count > 0:
            print(f"⚠️  Database already contains {existing_count} medicines. Skipping seed.")
            return
        
        medicines = seed_medicines()
        seed_sales(medicines)
        seed_purchase_orders(medicines)
        
        print("\n✅ Database seeding completed successfully!\n")
        
    except Exception as e:
        print(f"❌ Error during seeding: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
