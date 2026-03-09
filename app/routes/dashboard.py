from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models import Medicine, Sales, PurchaseOrder
from app.schemas import DailySalesSummary, LowStockItem, PurchaseOrderSummary

router = APIRouter(
    prefix="/api/dashboard",
    tags=["dashboard"]
)


@router.get("/sales-summary", response_model=DailySalesSummary)
def get_today_sales_summary(db: Session = Depends(get_db)):
    """
    Get today's sales summary including:
    - Total sales amount
    - Total items sold
    - Number of transactions
    """
    today = datetime.utcnow().date()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())
    
    sales_query = db.query(Sales).filter(
        and_(
            Sales.sale_date >= today_start,
            Sales.sale_date <= today_end
        )
    )
    
    total_sales = db.query(func.sum(Sales.quantity_sold * Sales.sale_price)).filter(
        and_(
            Sales.sale_date >= today_start,
            Sales.sale_date <= today_end
        )
    ).scalar() or 0.0
    
    items_sold = db.query(func.sum(Sales.quantity_sold)).filter(
        and_(
            Sales.sale_date >= today_start,
            Sales.sale_date <= today_end
        )
    ).scalar() or 0
    
    transactions_count = sales_query.count()
    
    return DailySalesSummary(
        total_sales=float(total_sales),
        items_sold=int(items_sold),
        transactions_count=transactions_count,
        date=today.isoformat()
    )


@router.get("/total-items-sold")
def get_total_items_sold(db: Session = Depends(get_db)):
    """
    Get total number of items sold (all time)
    """
    total = db.query(func.sum(Sales.quantity_sold)).scalar() or 0
    
    return {
        "total_items_sold": int(total),
        "message": "Total items sold across all time"
    }


@router.get("/low-stock-items", response_model=list[LowStockItem])
def get_low_stock_items(db: Session = Depends(get_db)):
    """
    Get all medicines with stock below reorder level
    """
    low_stock_medicines = db.query(Medicine).filter(
        Medicine.stock_quantity <= Medicine.reorder_level,
        Medicine.is_active == 1
    ).all()
    
    return [
        LowStockItem(
            id=medicine.id,
            name=medicine.name,
            current_stock=medicine.stock_quantity,
            reorder_level=medicine.reorder_level
        )
        for medicine in low_stock_medicines
    ]


@router.get("/purchase-order-summary", response_model=PurchaseOrderSummary)
def get_purchase_order_summary(db: Session = Depends(get_db)):
    """
    Get summary of purchase orders:
    - Count of pending orders
    - Count of delivered orders
    - Total quantity in pending orders
    """
    pending_orders = db.query(PurchaseOrder).filter(
        PurchaseOrder.status == "pending"
    ).count()
    
    delivered_orders = db.query(PurchaseOrder).filter(
        PurchaseOrder.status == "delivered"
    ).count()
    
    pending_quantity = db.query(func.sum(PurchaseOrder.quantity_ordered)).filter(
        PurchaseOrder.status == "pending"
    ).scalar() or 0
    
    return PurchaseOrderSummary(
        pending_orders=pending_orders,
        delivered_orders=delivered_orders,
        total_quantity_pending=int(pending_quantity)
    )
