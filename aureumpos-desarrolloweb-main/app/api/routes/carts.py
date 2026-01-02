from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from decimal import Decimal
from app.database import get_db
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.schemas.cart import CartItemCreate, CartItemUpdate, CartResponse, CartItemResponse
from app.api.deps import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/carts", tags=["carritos"])


def get_or_create_cart(user_id: int, db: Session) -> Cart:
    """Obtener o crear el carrito del usuario"""
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


@router.get("", response_model=CartResponse)
def get_cart(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener el carrito del usuario actual"""
    cart = get_or_create_cart(current_user.id, db)
    
    # Calcular total y preparar items
    items_response = []
    total = Decimal("0.00")
    
    for item in cart.items:
        # Actualizar precio si el producto cambió de precio
        if item.product.price != item.unit_price:
            item.unit_price = item.product.price
        
        subtotal = item.unit_price * item.quantity
        total += subtotal
        
        items_response.append(CartItemResponse(
            id=item.id,
            product_id=item.product_id,
            product=item.product,
            quantity=item.quantity,
            unit_price=item.unit_price,
            subtotal=subtotal
        ))
    
    # Guardar cambios de precio si hubo
    db.commit()
    
    return CartResponse(
        id=cart.id,
        user_id=cart.user_id,
        items=items_response,
        total=total,
        created_at=cart.created_at,
        updated_at=cart.updated_at
    )


@router.post("/items", response_model=CartResponse)
def add_item_to_cart(
    item_data: CartItemCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Agregar un producto al carrito"""
    # Verificar que el producto existe
    product = db.query(Product).filter(Product.id == item_data.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    
    if item_data.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La cantidad debe ser mayor a 0"
        )
    
    cart = get_or_create_cart(current_user.id, db)
    
    # Verificar si el producto ya está en el carrito
    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == item_data.product_id
    ).first()
    
    if existing_item:
        # Actualizar cantidad
        existing_item.quantity += item_data.quantity
        existing_item.unit_price = product.price  # Actualizar precio
        db.commit()
        db.refresh(existing_item)
    else:
        # Crear nuevo item
        new_item = CartItem(
            cart_id=cart.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity,
            unit_price=product.price
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    
    # Retornar carrito actualizado
    return get_cart(current_user, db)


@router.put("/items/{item_id}", response_model=CartResponse)
def update_cart_item(
    item_id: int,
    item_data: CartItemUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Actualizar la cantidad de un item en el carrito"""
    cart = get_or_create_cart(current_user.id, db)
    
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item no encontrado en el carrito"
        )
    
    if item_data.quantity is not None:
        if item_data.quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La cantidad debe ser mayor a 0"
            )
        cart_item.quantity = item_data.quantity
        # Actualizar precio del producto
        cart_item.unit_price = cart_item.product.price
    
    db.commit()
    
    return get_cart(current_user, db)


@router.delete("/items/{item_id}", response_model=CartResponse)
def remove_item_from_cart(
    item_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Eliminar un item del carrito"""
    cart = get_or_create_cart(current_user.id, db)
    
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item no encontrado en el carrito"
        )
    
    db.delete(cart_item)
    db.commit()
    
    return get_cart(current_user, db)


@router.delete("", response_model=CartResponse)
def clear_cart(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Vaciar el carrito completamente"""
    cart = get_or_create_cart(current_user.id, db)
    
    # Eliminar todos los items
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()
    
    return get_cart(current_user, db)

