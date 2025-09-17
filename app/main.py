import time 
from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from app.core import init_db
from app.core.exceptions import OrderProcessingError,order_exception_handler
from app.routes import users
from app.routes import products,orders



app= FastAPI()

@app.middleware("http")
async def log_requests(request:Request, call_next):
  start_time = time.time()

  response = await call_next(request)

  process_time = time.time() - start_time
  print(f"{request.method} {request.url.path} completed in {process_time:.4f}s")
  return response

@app.middleware("http")
async def catch_exceptions_middleware(request:Request, call_next):
  try:
    return await call_next(request)
  except Exception as exc:
    print(f"Unexpected error: {exc}")
    return JSONResponse(
      status_code=500,
      content={"error":"Internal server error. Please try again later."}
    )

@app.on_event("startup")
async def on_startup():
  await init_db()

app.add_exception_handler(OrderProcessingError,order_exception_handler)

app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)



@app.get("/")
async def read_root():
  return{"message": "E-commerce API- up and running"}




  