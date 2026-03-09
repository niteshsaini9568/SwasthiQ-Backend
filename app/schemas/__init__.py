from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# Medicine Schemas
class MedicineBase(BaseModel):
    """Base schema for Medicine"""
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int = 0
    reorder_level: int = 50
    category: str
    manufacturer: str
    expiry_date: Optional[datetime] = None


class MedicineCreate(MedicineBase):
    """Schema for creating a new medicine"""
    pass


class MedicineUpdate(BaseModel):
    """Schema for updating a medicine"""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    reorder_level: Optional[int] = None
    category: Optional[str] = None
    manufacturer: Optional[str] = None
    expiry_date: Optional[datetime] = None


class MedicineResponse(MedicineBase):
    """Schema for medicine response"""
    id: int
    is_active: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Sales Schemas
class SalesBase(BaseModel):
    """Base schema for Sales"""
    medicine_id: int
    quantity_sold: int
    sale_price: float


class SalesCreate(SalesBase):
    """Schema for creating a new sale"""
    pass


class SalesResponse(SalesBase):
    """Schema for sales response"""
    id: int
    sale_date: datetime
    created_at: datetime
    medicine: MedicineResponse
    
    class Config:
        from_attributes = True


# Purchase Order Schemas
class PurchaseOrderBase(BaseModel):
    """Base schema for Purchase Order"""
    medicine_id: int
    quantity_ordered: int
    expected_delivery_date: Optional[datetime] = None


class PurchaseOrderCreate(PurchaseOrderBase):
    """Schema for creating a new purchase order"""
    pass


class PurchaseOrderUpdate(BaseModel):
    """Schema for updating a purchase order"""
    status: Optional[str] = None


class PurchaseOrderResponse(PurchaseOrderBase):
    """Schema for purchase order response"""
    id: int
    order_date: datetime
    status: str
    created_at: datetime
    updated_at: datetime
    medicine: MedicineResponse
    
    class Config:
        from_attributes = True


# Dashboard Schemas
class DailySalesSummary(BaseModel):
    """Schema for daily sales summary"""
    total_sales: float
    items_sold: int
    transactions_count: int
    date: str


class LowStockItem(BaseModel):
    """Schema for low stock items"""
    id: int
    name: str
    current_stock: int
    reorder_level: int
    
    class Config:
        from_attributes = True


class PurchaseOrderSummary(BaseModel):
    """Schema for purchase order summary"""
    pending_orders: int
    delivered_orders: int
    total_quantity_pending: int
