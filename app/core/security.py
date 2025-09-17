from fastapi import Depends, HTTPException,status
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User
from app.core import get_db
from typing import List
from fastapi import Security
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt,JWTError
from typing import Optional
from dotenv import load_dotenv
import os



load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM","HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
api_key_scheme = APIKeyHeader(name="Authorization")

def get_password_hash(password: str) -> str:
  return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str)-> bool:
  return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data:dict, expires_delta:Optional[timedelta] = None)->str:
  to_encode= data.copy()
  if expires_delta:
    expires = datetime.utcnow() + expires_delta
  else:
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp":expires})
  encodes_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
  return encodes_jwt

def verify_token(token:str) -> dict:
  try:
    payload = jwt.decode(token, SECRET_KEY,algorithms=ALGORITHM)
    return payload
  except JWTError as e:
    raise JWTError(f"Token is invalid or expired: {e}")

async def get_current_user(token:str = Depends(api_key_scheme), db:AsyncSession = Depends(get_db)) -> User:
  if token.startswith("Bearer"):
    token= token[7:]
  else:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid token prefix, expected 'Bearer '",
    )
  try:
    payload = verify_token(token)
    user_id: str = payload.get("sub")
    if user_id is None:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
      )
  except JWTError:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        )
  result = await db.execute(select(User).where(User.id == int(user_id)))
  user = result.scalars().first()
  if user is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="User not found"
    )
  return user

def required_role(reuired_roles: List[str]):
  async def role_checker(current_user: User = Depends(get_current_user)):
    if current_user.role not in reuired_roles:
      raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to access this resource"
      )
    return current_user
  return role_checker



