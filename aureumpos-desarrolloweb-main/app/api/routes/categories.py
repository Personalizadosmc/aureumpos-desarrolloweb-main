from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.category import Category
from app.models.product import Product
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.api.deps import get_current_admin
from app.models.user import User

router = APIRouter(prefix="/categories", tags=["categorías"])


@router.get("", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """Obtener todas las categorías con conteo de productos"""
    categories = db.query(Category).all()
    result = []
    for category in categories:
        product_count = db.query(Product).filter(Product.category_id == category.id).count()
        category_dict = {
            **category.__dict__,
            "product_count": product_count
        }
        result.append(CategoryResponse(**category_dict))
    return result


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Obtener una categoría por ID"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    product_count = db.query(Product).filter(Product.category_id == category.id).count()
    category_dict = {
        **category.__dict__,
        "product_count": product_count
    }
    return CategoryResponse(**category_dict)


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Crear una nueva categoría (solo administradores)"""
    # Verificar si ya existe una categoría con ese nombre
    existing = db.query(Category).filter(Category.name == category_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una categoría con ese nombre"
        )
    
    new_category = Category(**category_data.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    category_dict = {
        **new_category.__dict__,
        "product_count": 0
    }
    return CategoryResponse(**category_dict)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Actualizar una categoría (solo administradores)"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    
    # Verificar nombre único si se está cambiando
    if category_data.name and category_data.name != category.name:
        existing = db.query(Category).filter(Category.name == category_data.name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una categoría con ese nombre"
            )
    
    # Actualizar campos
    update_data = category_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)
    
    db.commit()
    db.refresh(category)
    
    product_count = db.query(Product).filter(Product.category_id == category.id).count()
    category_dict = {
        **category.__dict__,
        "product_count": product_count
    }
    return CategoryResponse(**category_dict)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Eliminar una categoría (solo administradores)"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    
    # Verificar si tiene productos asociados
    product_count = db.query(Product).filter(Product.category_id == category.id).count()
    if product_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede eliminar la categoría porque tiene {product_count} producto(s) asociado(s)"
        )
    
    db.delete(category)
    db.commit()
    return None

