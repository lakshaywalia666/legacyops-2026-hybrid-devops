from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ProductCreate(BaseModel):
    sku: str = Field(..., min_length=2, max_length=80)
    name: str = Field(..., min_length=2, max_length=200)
    category: Optional[str] = Field(default=None, max_length=120)
    unit_price: float = Field(..., gt=0)
    stock_quantity: int = Field(default=0, ge=0)


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sku: str
    name: str
    category: Optional[str]
    unit_price: float
    stock_quantity: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class CustomerCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, max_length=40)
    address: Optional[str] = None


class CustomerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    created_at: datetime


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    customer_id: int
    items: List[OrderItemCreate] = Field(..., min_length=1)


class OrderItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    unit_price: float
    line_total: float


class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    status: str
    total_amount: float
    created_at: datetime
    items: List[OrderItemRead]


class InventoryEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    event_type: str
    quantity_delta: int
    reason: Optional[str]
    created_at: datetime


class DashboardSummary(BaseModel):
    products: int
    customers: int
    orders: int
    low_stock_products: int
    total_revenue: float
    pending_orders: int
