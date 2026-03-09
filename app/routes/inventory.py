from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from datetime import datetime
from app.core.database import get_db
from app.models import Medicine, Sales
from app.schemas import MedicineCreate, MedicineUpdate, MedicineResponse, SalesCreate, SalesResponse

router = APIRouter(
    prefix="/api/inventory",
    tags=["inventory"]
)


@router.get("/medicines", response_model=list[MedicineResponse])
def list_medicines(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: str = Query(None),
    search: str = Query(None)
):
    """
    List all medicines with optional filtering and search
    
    Query Parameters:
    - skip: Number of records to skip (for pagination)
    - limit: Number of records to return (default 10, max 100)
    - category: Filter by category
    - search: Search by name, description, or manufacturer
    """
    query = db.query(Medicine)
    
    # Filter by category if provided
    if category:
        query = query.filter(Medicine.category == category)
    
    # Search by name, description, or manufacturer
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Medicine.name.ilike(search_term),
                Medicine.description.ilike(search_term),
                Medicine.manufacturer.ilike(search_term)
            )
        )
    
    medicines = query.offset(skip).limit(limit).all()
    return medicines


@router.get("/medicines/{medicine_id}", response_model=MedicineResponse)
def get_medicine_detail(medicine_id: int, db: Session = Depends(get_db)):
    """
    Get details of a specific medicine
    """
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    
    return medicine


@router.post("/medicines", response_model=MedicineResponse)
def add_medicine(
    medicine: MedicineCreate,
    db: Session = Depends(get_db)
):
    """
    Add a new medicine to inventory
    """
    # Check if medicine already exists
    existing = db.query(Medicine).filter(Medicine.name == medicine.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Medicine with this name already exists")
    
    db_medicine = Medicine(**medicine.dict())
    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)
    
    return db_medicine


@router.put("/medicines/{medicine_id}", response_model=MedicineResponse)
def update_medicine(
    medicine_id: int,
    medicine: MedicineUpdate,
    db: Session = Depends(get_db)
):
    """
    Update medicine details
    """
    db_medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    
    if not db_medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    
    update_data = medicine.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_medicine, field, value)
    
    db_medicine.updated_at = datetime.utcnow()
    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)
    
    return db_medicine


@router.patch("/medicines/{medicine_id}/mark-expired")
def mark_expired(medicine_id: int, db: Session = Depends(get_db)):
    """
    Mark a medicine as expired (mark as inactive)
    """
    db_medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    
    if not db_medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    
    db_medicine.is_active = 0
    db_medicine.updated_at = datetime.utcnow()
    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)
    
    return {
        "message": "Medicine marked as expired",
        "medicine": db_medicine
    }


@router.patch("/medicines/{medicine_id}/mark-out-of-stock")
def mark_out_of_stock(medicine_id: int, db: Session = Depends(get_db)):
    """
    Mark a medicine as out of stock
    """
    db_medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    
    if not db_medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    
    db_medicine.stock_quantity = 0
    db_medicine.is_active = 0
    db_medicine.updated_at = datetime.utcnow()
    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)
    
    return {
        "message": "Medicine marked as out of stock",
        "medicine": db_medicine
    }


@router.get("/medicines/by/category/{category}")
def get_medicines_by_category(
    category: str,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """
    Get medicines filtered by category with pagination
    """
    medicines = db.query(Medicine).filter(
        Medicine.category == category
    ).offset(skip).limit(limit).all()
    
    if not medicines:
        raise HTTPException(status_code=404, detail="No medicines found in this category")
    
    return medicines


@router.get("/medicines/search/{search_term}")
def search_medicines(
    search_term: str,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """
    Search medicines by name, description, or manufacturer
    """
    search_pattern = f"%{search_term}%"
    
    medicines = db.query(Medicine).filter(
        or_(
            Medicine.name.ilike(search_pattern),
            Medicine.description.ilike(search_pattern),
            Medicine.manufacturer.ilike(search_pattern)
        )
    ).offset(skip).limit(limit).all()
    
    if not medicines:
        raise HTTPException(status_code=404, detail="No medicines found matching the search term")
    
    return medicines


@router.post("/sales", response_model=SalesResponse)
def record_sale(
    sale: SalesCreate,
    db: Session = Depends(get_db)
):
    """
    Record a medicine sale and deduct from stock
    """
    medicine = db.query(Medicine).filter(Medicine.id == sale.medicine_id).first()
    
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    
    if medicine.stock_quantity < sale.quantity_sold:
        raise HTTPException(status_code=400, detail="Insufficient stock available")
    
    # Create sales record
    db_sale = Sales(**sale.dict())
    db.add(db_sale)
    
    # Update medicine stock
    medicine.stock_quantity -= sale.quantity_sold
    db.add(medicine)
    
    db.commit()
    db.refresh(db_sale)
    
    return db_sale


@router.get("/categories")
def get_all_categories(db: Session = Depends(get_db)):
    """
    Get all medicine categories
    """
    categories = db.query(Medicine.category).distinct().all()
    
    return {
        "categories": [cat[0] for cat in categories]
    }


@router.get("/stats")
def get_inventory_stats(db: Session = Depends(get_db)):
    """
    Get inventory statistics
    """
    total_medicines = db.query(Medicine).count()
    active_medicines = db.query(Medicine).filter(Medicine.is_active == 1).count()
    total_stock = db.query(Medicine).filter(Medicine.is_active == 1).all()
    total_stock_quantity = sum(m.stock_quantity for m in total_stock)
    total_stock_value = sum(m.stock_quantity * m.price for m in total_stock)
    
    return {
        "total_medicines": total_medicines,
        "active_medicines": active_medicines,
        "total_stock_quantity": total_stock_quantity,
        "total_stock_value": total_stock_value
    }
