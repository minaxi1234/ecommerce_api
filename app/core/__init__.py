from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
print("Database URL:", DATABASE_URL)

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

engine = create_async_engine(DATABASE_URL, echo = True)

from app.models import Base

AsyncSessionLocal = sessionmaker(bind=engine,class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
  async with AsyncSessionLocal() as session:
    yield session

async def init_db():
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)

