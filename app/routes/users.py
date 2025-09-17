from fastapi import APIRouter,Depends,HTTPException,status,Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas import UserCreate,UserLogin,UserRead
from app.models import User
from app.core.security import verify_password,create_access_token,get_password_hash,get_current_user, required_role
from app.core import get_db

router = APIRouter(
  prefix= "/users", tags=["Users"]
)

@router.get("/me")
async def read_profile(current_user:User = Depends(get_current_user)):
  return{
    "id": current_user.id,
    "name": current_user.name,
    "email": current_user.email
  }

@router.post("/register", response_model=UserRead,status_code=status.HTTP_201_CREATED)
async def get_users(user:UserCreate = Body(...), db:AsyncSession=Depends(get_db)):
  result = await db.execute(select(User).where(User.email == user.email))
  existing_user=result.scalars().first()
  if existing_user:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail='Email already exists'
    )
  hashed_password = get_password_hash(user.password)

  new_user= User(
    name= user.name,
    email= user.email,
    password= hashed_password,
    role = user.role
  )  

  db.add(new_user)
  await db.commit()
  await db.refresh(new_user)
  return new_user

@router.post("/")
async def login(user:UserLogin, db:AsyncSession= Depends(get_db)):
  result = await db.execute(
    select(User).where(User.email == user.email)
  )
  db_user = result.scalars().first()  

  if not db_user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid email or password"
    )
  if not verify_password(user.password,db_user.password):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid email or password"
    )
  access_token = create_access_token(data={"sub": str(db_user.id)})
  return {"access_token": access_token, "token_type":"bearer"}

@router.get("/admin-only")
async def admin_dashboard(current_user: User = Depends(required_role(["admin"]))):
  return {"message": f"Hello Admin {current_user.name}!"}








