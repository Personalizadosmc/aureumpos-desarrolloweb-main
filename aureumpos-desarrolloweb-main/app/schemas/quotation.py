from pydantic import BaseModel
from datetime import datetime
from typing import List
from decimal import Decimal


class QuotationItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    quantity: int
    unit_price: Decimal
    subtotal: Decimal

    class Config:
        from_attributes = True


class QuotationBase(BaseModel):
    pass


class QuotationCreate(QuotationBase):
    pass


class QuotationResponse(BaseModel):
    id: int
    quotation_number: str
    user_id: int
    total_amount: Decimal
    items: List[QuotationItemResponse]
    created_at: datetime

    class Config:
        from_attributes = True


class Quotation(QuotationResponse):
    pass

