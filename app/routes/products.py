from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Product
from app.schemas import ProductCreate, ProductBase,ProductRead
from app.core import get_db
from app.core.security import required_role

router = APIRouter(
  prefix="/products",
  tags=["Products"]
)

@router.post("/", response_model=ProductRead)
async def create_product(product:ProductCreate,db:AsyncSession=Depends(get_db),current_user=Depends(required_role(["admin"]))):
  new_product= Product(
    name = product.name,
    description= product.description,
    price = product.price,
    stock= product.stock
  )
  db.add(new_product)
  await db.commit()
  await db.refresh(new_product)
  return new_product

#Read all products
@router.get("/",response_model=list[ProductRead])
async def all_products(db:AsyncSession=Depends(get_db)):
  result= await db.execute(select(Product))
  products= result.scalars().all()
  return products

#Read a single product by id 
@router.get("/{product_id}",response_model=ProductRead)
async def get_product_by_id(product_id:int,db:AsyncSession=Depends(get_db)):
  result= await db.execute(select(Product).where(Product.id == product_id))
  product = result.scalars().first()
  if not product:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Product not found"
    )
  return product
  
# Update a product(Admin only)
@router.put("/{product_id}",response_model=ProductRead)
async def update_product(product_id:int, 
updated_product:ProductCreate,db:AsyncSession=Depends(get_db),current_user=Depends(required_role(["admin"]))):
  result = await db.execute(select(Product).where(Product.id == product_id))
  product = result.scalars().first()
  if not product:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Product not found"
    )
  product.name = updated_product.name
  product.description= updated_product.description
  product.price= updated_product.price
  product.stock=updated_product.stock

  db.add(product)
  await db.commit()
  await db.refresh(product)
  return product

# DELETE a product by ID (admin only)
@router.delete("/{product_id}")
async def delete_product(product_id:int,db:AsyncSession=Depends(get_db),current_user=Depends(required_role(["admin"]))):
  result= await db.execute(select(Product).where(Product.id == product_id))
  product= result.scalars().first()
  if not product:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Product not found"
    )
  await db.delete(product)
  await db.commit()
  return {"detail": "Product deleted successfully"}

