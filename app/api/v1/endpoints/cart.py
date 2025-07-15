from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.schemas.cart import CartResponse, CartItemCreate, CartItemUpdate

router = APIRouter()


@router.get("/", response_model=CartResponse)
def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get current user's cart
    """
    cart = db.query(Cart).filter(Cart.user_id == current_user.user_id).first()
    if not cart:
        # Create cart if it doesn't exist
        cart = Cart(user_id=current_user.user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    
    return cart


@router.post("/items", response_model=CartResponse)
def add_item_to_cart(
    item_in: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Add item to cart
    """
    # Get or create cart
    cart = db.query(Cart).filter(Cart.user_id == current_user.user_id).first()
    if not cart:
        cart = Cart(user_id=current_user.user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    
    # Check if product exists and is active
    product = db.query(Product).filter(
        Product.product_id == item_in.product_id,
        Product.is_active == True
    ).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Check if product is in stock
    if product.stock_quantity < item_in.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only {product.stock_quantity} items available in stock"
        )
    
    # Check if item already exists in cart
    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.cart_id,
        CartItem.product_id == item_in.product_id
    ).first()
    
    if existing_item:
        # Update quantity if item already exists
        new_quantity = existing_item.quantity + item_in.quantity
        if product.stock_quantity < new_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Only {product.stock_quantity} items available in stock"
            )
        existing_item.quantity = new_quantity
    else:
        # Add new item to cart
        cart_item = CartItem(
            cart_id=cart.cart_id,
            product_id=item_in.product_id,
            quantity=item_in.quantity
        )
        db.add(cart_item)
    
    db.commit()
    db.refresh(cart)
    
    return cart


@router.put("/items/{cart_item_id}", response_model=CartResponse)
def update_cart_item(
    cart_item_id: int,
    item_update: CartItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Update cart item quantity
    """
    # Get cart item and verify ownership
    cart_item = db.query(CartItem).join(Cart).filter(
        CartItem.cart_item_id == cart_item_id,
        Cart.user_id == current_user.user_id
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    # Check stock availability
    if cart_item.product.stock_quantity < item_update.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only {cart_item.product.stock_quantity} items available in stock"
        )
    
    cart_item.quantity = item_update.quantity
    db.commit()
    db.refresh(cart_item.cart)
    
    return cart_item.cart


@router.delete("/items/{cart_item_id}", response_model=CartResponse)
def remove_cart_item(
    cart_item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Remove item from cart
    """
    # Get cart item and verify ownership
    cart_item = db.query(CartItem).join(Cart).filter(
        CartItem.cart_item_id == cart_item_id,
        Cart.user_id == current_user.user_id
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    cart = cart_item.cart
    db.delete(cart_item)
    db.commit()
    db.refresh(cart)
    
    return cart


@router.delete("/clear", response_model=CartResponse)
def clear_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Clear all items from cart
    """
    cart = db.query(Cart).filter(Cart.user_id == current_user.user_id).first()
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )
    
    # Delete all cart items
    db.query(CartItem).filter(CartItem.cart_id == cart.cart_id).delete()
    db.commit()
    db.refresh(cart)
    
    return cart