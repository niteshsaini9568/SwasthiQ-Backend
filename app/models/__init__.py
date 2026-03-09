from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base


class Medicine(Base):
    """Medicine/Product model"""
    __tablename__ = "medicines"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, unique=True, nullable=False)
    description = Column(String(1000), nullable=True)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    reorder_level = Column(Integer, default=50)  # Threshold for low stock
    category = Column(String(100), index=True, nullable=False)
    manufacturer = Column(String(255), nullable=False)
    expiry_date = Column(DateTime, nullable=True)
    is_active = Column(Integer, default=1)  # 1 = active, 0 = expired/out of stock
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sales = relationship("Sales", back_populates="medicine", cascade="all, delete-orphan")
    purchase_orders = relationship("PurchaseOrder", back_populates="medicine", cascade="all, delete-orphan")


class Sales(Base):
    """Sales/Transaction model"""
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, index=True)
    medicine_id = Column(Integer, ForeignKey("medicines.id"), nullable=False)
    quantity_sold = Column(Integer, nullable=False)
    sale_price = Column(Float, nullable=False)
    sale_date = Column(DateTime, default=datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    medicine = relationship("Medicine", back_populates="sales")


class PurchaseOrder(Base):
    """Purchase Order model"""
    __tablename__ = "purchase_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    medicine_id = Column(Integer, ForeignKey("medicines.id"), nullable=False)
    quantity_ordered = Column(Integer, nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow, index=True)
    expected_delivery_date = Column(DateTime, nullable=True)
    status = Column(String(50), default="pending")  # pending, delivered, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    medicine = relationship("Medicine", back_populates="purchase_orders")
