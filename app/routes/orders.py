from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User,Product,Order,OrderItem
from app.schemas import OrderBase,OrderCreate,OrderItemBase,OrderStatusUpdate,OrderItemCreate,OrderItemRead,OrderRead
from app.core import get_db
from app.core.security import get_current_user,required_role
from app.core.exceptions import OrderProcessingError


router = APIRouter(
  prefix="/orders",
  tags=["Orders"]
)



@router.post("/", response_model=OrderRead)
async def create_order(
    order:OrderCreate,
    db:AsyncSession= Depends(get_db),
    current_user:User = Depends(get_current_user)
):
    new_order= Order(user_id = current_user.id)

    db.add(new_order)
    await db.flush()

    total =0.0

    for item in order.items:
        result =  await db.execute(select(Product).where(Product.id == item.product_id))
        product = result.scalars().first()
        if not product:
            raise OrderProcessingError(detail=f"Product {item.product_id} not found")
        
        order_item = OrderItem(
            order_id = new_order.id,
            product_id = product.id,
            quantity = item.quantity,
            price = product.price
        )
        db.add(order_item)
        total += product.price * item.quantity

        new_order.total_amount = total

        await db.commit()
        await db.refresh(new_order)
        return new_order
    
@router.get("/", response_model=list[OrderRead])
async def get_orders(
    db:AsyncSession = Depends(get_db),
    current_user:User = Depends(get_current_user)
):
    result = await db.execute(select(Order).where(Order.user_id == current_user.id))
    orders = result.scalars().unique().all()
    return orders

@router.get("/{order_id}",response_model=OrderRead)
async def get_order_by_id(
    order_id:int,
    db:AsyncSession= Depends(get_db),
    current_user: User= Depends(get_current_user)
):
    result = await db.execute(select(Order).where(Order.id == order_id, Order.user_id == current_user.id))
    order = result.scalars().first()
    if not order:
        raise OrderProcessingError(detail="Order not found")
    return order
    
@router.patch("/{order_id}/status", response_model=OrderRead)
async def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    db: AsyncSession= Depends(get_db),
    current_user:User=Depends(required_role(["admin"]))
):
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()
    if not order:
        raise OrderProcessingError(detail="Order not found" )
    order.status = status_update.status
    await db.commit()
    await db.refresh(order)
    return order





