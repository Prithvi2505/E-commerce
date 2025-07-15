from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.core.database import get_db
from app.core.security import get_current_user, get_current_admin_user
from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.schemas.product import (
    ProductCreate, ProductUpdate, ProductResponse, 
    ProductListResponse, ProductSearch
)

router = APIRouter()


@router.get("/", response_model=ProductListResponse)
def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    in_stock_only: bool = Query(True),
    sort_by: str = Query("name", regex="^(name|price|created_at|rating)$"),
    sort_order: str = Query("asc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
) -> Any:
    """
    Retrieve products with filtering and pagination
    """
    query = db.query(Product).filter(Product.is_active == True)
    
    # Apply filters
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            or_(
                Product.name.ilike(search_filter),
                Product.description.ilike(search_filter)
            )
        )
    
    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    
    if in_stock_only:
        query = query.filter(Product.stock_quantity > 0)
    
    # Apply sorting
    if sort_by == "name":
        query = query.order_by(Product.name.asc() if sort_order == "asc" else Product.name.desc())
    elif sort_by == "price":
        query = query.order_by(Product.price.asc() if sort_order == "asc" else Product.price.desc())
    elif sort_by == "created_at":
        query = query.order_by(Product.created_at.asc() if sort_order == "asc" else Product.created_at.desc())
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    products = query.offset(skip).limit(limit).all()
    
    # Calculate pagination info
    pages = (total + limit - 1) // limit
    
    return {
        "products": products,
        "total": total,
        "page": (skip // limit) + 1,
        "pages": pages,
        "per_page": limit
    }


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
) -> Any:
    """
    Get product by ID
    """
    product = db.query(Product).filter(
        and_(Product.product_id == product_id, Product.is_active == True)
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product


@router.post("/", response_model=ProductResponse)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
) -> Any:
    """
    Create new product (Admin only)
    """
    # Check if category exists
    category = db.query(Category).filter(Category.category_id == product_in.category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not found"
        )
    
    # Check if SKU already exists
    if product_in.sku:
        existing_product = db.query(Product).filter(Product.sku == product_in.sku).first()
        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product with this SKU already exists"
            )
    
    product = Product(**product_in.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    
    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
) -> Any:
    """
    Update product (Admin only)
    """
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Check if category exists (if being updated)
    if product_in.category_id:
        category = db.query(Category).filter(Category.category_id == product_in.category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category not found"
            )
    
    # Check if SKU already exists (if being updated)
    if product_in.sku and product_in.sku != product.sku:
        existing_product = db.query(Product).filter(Product.sku == product_in.sku).first()
        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product with this SKU already exists"
            )
    
    # Update product
    update_data = product_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    
    return product


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
) -> Any:
    """
    Delete product (Admin only) - Soft delete by setting is_active to False
    """
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    product.is_active = False
    db.commit()
    
    return {"message": "Product deleted successfully"}


@router.get("/search/", response_model=ProductListResponse)
def search_products(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
) -> Any:
    """
    Search products by name and description
    """
    search_filter = f"%{q}%"
    query = db.query(Product).filter(
        and_(
            Product.is_active == True,
            or_(
                Product.name.ilike(search_filter),
                Product.description.ilike(search_filter)
            )
        )
    )
    
    total = query.count()
    products = query.offset(skip).limit(limit).all()
    pages = (total + limit - 1) // limit
    
    return {
        "products": products,
        "total": total,
        "page": (skip // limit) + 1,
        "pages": pages,
        "per_page": limit
    }