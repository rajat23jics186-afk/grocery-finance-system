"""Product routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from backend.database import get_db
from backend.models.product import Product

router = APIRouter(prefix="/api/products", tags=["Products"])


class ProductCreate(BaseModel):
    """Product creation schema."""
    name: str
    category: str
    description: Optional[str] = None
    retail_price: float
    wholesale_price: float
    quantity_in_stock: int = 0
    reorder_level: int = 10
    supplier: Optional[str] = None


class ProductUpdate(BaseModel):
    """Product update schema."""
    name: Optional[str] = None
    description: Optional[str] = None
    retail_price: Optional[float] = None
    wholesale_price: Optional[float] = None
    quantity_in_stock: Optional[int] = None
    reorder_level: Optional[int] = None
    supplier: Optional[str] = None


@router.post("/", response_model=dict)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product."""
    existing = db.query(Product).filter(Product.name == product_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Product already exists")
    
    db_product = Product(**product_data.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return {"id": db_product.id, "name": db_product.name, "message": "Product created"}


@router.get("/")
def list_products(category: Optional[str] = None, db: Session = Depends(get_db)):
    """List all products, optionally filtered by category."""
    query = db.query(Product)
    if category:
        query = query.filter(Product.category == category)
    return query.all()


@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get single product by ID."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}")
def update_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    """Update product."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product_data.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete product."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}
