from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from decimal import Decimal
from datetime import datetime
import io
from app.database import get_db
from app.models.quotation import Quotation, QuotationItem
from app.models.cart import Cart, CartItem
from app.models.user import User
from app.schemas.quotation import QuotationResponse, QuotationItemResponse
from app.api.deps import get_current_active_user
from app.core.pdf_generator import generate_quotation_pdf

router = APIRouter(prefix="/quotations", tags=["cotizaciones"])


def generate_quotation_number() -> str:
    """Generar un número único de cotización"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"COT-{timestamp}"


@router.post("", response_model=QuotationResponse, status_code=status.HTTP_201_CREATED)
def create_quotation(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Crear una cotización a partir del carrito actual"""
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    
    if not cart or not cart.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El carrito está vacío"
        )
    
    # Calcular total
    total_amount = Decimal("0.00")
    quotation_items = []
    
    for cart_item in cart.items:
        # Usar precio actualizado del producto
        unit_price = cart_item.product.price
        subtotal = unit_price * cart_item.quantity
        total_amount += subtotal
        
        # Crear item de cotización
        quotation_item = QuotationItem(
            product_id=cart_item.product_id,
            product_name=cart_item.product.name,
            quantity=cart_item.quantity,
            unit_price=unit_price,
            subtotal=subtotal
        )
        quotation_items.append(quotation_item)
    
    # Crear cotización
    quotation_number = generate_quotation_number()
    new_quotation = Quotation(
        quotation_number=quotation_number,
        user_id=current_user.id,
        total_amount=total_amount,
        items=quotation_items
    )
    
    db.add(new_quotation)
    db.commit()
    db.refresh(new_quotation)
    
    # Preparar respuesta
    items_response = [
        QuotationItemResponse(
            id=item.id,
            product_id=item.product_id,
            product_name=item.product_name,
            quantity=item.quantity,
            unit_price=item.unit_price,
            subtotal=item.subtotal
        )
        for item in new_quotation.items
    ]
    
    return QuotationResponse(
        id=new_quotation.id,
        quotation_number=new_quotation.quotation_number,
        user_id=new_quotation.user_id,
        total_amount=new_quotation.total_amount,
        items=items_response,
        created_at=new_quotation.created_at
    )


@router.get("", response_model=List[QuotationResponse])
def get_user_quotations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener todas las cotizaciones del usuario actual"""
    quotations = db.query(Quotation).filter(
        Quotation.user_id == current_user.id
    ).order_by(Quotation.created_at.desc()).all()
    
    result = []
    for quotation in quotations:
        items_response = [
            QuotationItemResponse(
                id=item.id,
                product_id=item.product_id,
                product_name=item.product_name,
                quantity=item.quantity,
                unit_price=item.unit_price,
                subtotal=item.subtotal
            )
            for item in quotation.items
        ]
        result.append(QuotationResponse(
            id=quotation.id,
            quotation_number=quotation.quotation_number,
            user_id=quotation.user_id,
            total_amount=quotation.total_amount,
            items=items_response,
            created_at=quotation.created_at
        ))
    
    return result


@router.get("/{quotation_id}", response_model=QuotationResponse)
def get_quotation(
    quotation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener una cotización específica"""
    quotation = db.query(Quotation).filter(
        Quotation.id == quotation_id,
        Quotation.user_id == current_user.id
    ).first()
    
    if not quotation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cotización no encontrada"
        )
    
    items_response = [
        QuotationItemResponse(
            id=item.id,
            product_id=item.product_id,
            product_name=item.product_name,
            quantity=item.quantity,
            unit_price=item.unit_price,
            subtotal=item.subtotal
        )
        for item in quotation.items
    ]
    
    return QuotationResponse(
        id=quotation.id,
        quotation_number=quotation.quotation_number,
        user_id=quotation.user_id,
        total_amount=quotation.total_amount,
        items=items_response,
        created_at=quotation.created_at
    )


@router.get("/{quotation_id}/pdf")
def download_quotation_pdf(
    quotation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Descargar cotización en formato PDF"""
    quotation = db.query(Quotation).filter(
        Quotation.id == quotation_id,
        Quotation.user_id == current_user.id
    ).first()
    
    if not quotation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cotización no encontrada"
        )
    
    # Preparar items para PDF
    items_for_pdf = [
        QuotationItemResponse(
            id=item.id,
            product_id=item.product_id,
            product_name=item.product_name,
            quantity=item.quantity,
            unit_price=item.unit_price,
            subtotal=item.subtotal
        )
        for item in quotation.items
    ]
    
    # Generar PDF
    pdf_buffer = io.BytesIO()
    generate_quotation_pdf(
        quotation_number=quotation.quotation_number,
        user=current_user,
        items=items_for_pdf,
        total_amount=quotation.total_amount,
        output_buffer=pdf_buffer
    )
    
    pdf_buffer.seek(0)
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=cotizacion_{quotation.quotation_number}.pdf"
        }
    )

