from pydantic import BaseModel , EmailStr
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
  name: str
  email: EmailStr
  password: str
  role: str = "user"

class UserRead(BaseModel):
  id: int
  name: str
  email: EmailStr


  class Config:
   orm_mode = True

class UserLogin(BaseModel):
  email:EmailStr
  password:str

class ProductBase(BaseModel):
  name:str
  description:str | None=None
  price: float
  stock: int= 0

class ProductCreate(ProductBase):
  pass

class ProductRead(ProductBase):
  id:int

  class Config:
    orm_mode= True

class OrderItemBase(BaseModel):
  product_id: int
  quantity: int

class OrderItemCreate(OrderItemBase):
  pass

class OrderItemRead(OrderItemBase):
  id:int
  price:float
  product_id:int

  class Config:
    orm_mode = True

class OrderBase(BaseModel):
  status: Optional[str] = "pending"

class OrderCreate(OrderBase):
  items: List[OrderItemCreate]

class OrderRead(OrderBase):
  id:int
  user_id: int
  created_at: datetime
  total_amount: float
  items:List[OrderItemRead] = []

class OrderStatusUpdate(BaseModel):
  status: str

  class Config:
    orm_mode = True

class ErrorResponse(BaseModel):
  error:str
  detail:str | None = None
