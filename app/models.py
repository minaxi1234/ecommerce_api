from sqlalchemy import Column,Integer,String,Float,ForeignKey,DateTime,func
from sqlalchemy.orm import declarative_base,relationship

Base = declarative_base()

class User(Base):
  __tablename__ = "users"

  id= Column(Integer, primary_key=True, index=True)
  name= Column(String, nullable=False)
  email= Column(String, unique=True, index=True, nullable=False)
  password = Column(String, nullable=False)
  role = Column(String, default="user")

class Product(Base):
  __tablename__ = "products"
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, nullable=False)
  description = Column(String, nullable=True)
  price = Column(Float, nullable=False)
  stock = Column(Integer, default=0)

class Order(Base):
  __tablename__ = "orders"

  id= Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
  created_at= Column(DateTime(timezone=True), server_default= func.now())
  status = Column(String, default="pending")
  total_amount = Column(Float, default=0.0)

  user = relationship("User", backref="orders")
  items = relationship("OrderItem", back_populates="order", lazy="joined")

class OrderItem(Base):
  __tablename__ = "order_items"

  id = Column(Integer, primary_key=True, index=True)
  order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
  product_id= Column(Integer,ForeignKey("products.id"), nullable=False)
  quantity = Column(Integer, nullable=False)
  price = Column(Float, nullable=False)

  order = relationship("Order", back_populates="items", lazy="joined")
  product = relationship("Product", backref="order_items")



  
