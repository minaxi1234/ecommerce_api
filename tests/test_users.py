import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app

def test_example():
  assert 1 + 1 ==2

@pytest.mark.asyncio
async def test_root_endpoint():
  transport = ASGITransport(app=app)
  async with AsyncClient(transport=transport,base_url="http://test") as ac:
    response = await ac.get("/")
  assert response.status_code == 200

@pytest.mark.asyncio
async def test_user_registration():
  transport = ASGITransport(app= app)
  async with AsyncClient(transport=transport,base_url="http://test")as ac:
    payload = {
      "name" : "Test User",
      "email" : "helloo1111@example.com",#change the email everytime u test
      "password" : "1234"
    }
    response = await ac.post("/users/register", json=payload)

  assert response.status_code == 201
  data = response.json()
  assert data["email"] ==  "helloo1111@example.com"

