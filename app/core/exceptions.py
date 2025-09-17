from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from app.schemas import ErrorResponse

class OrderProcessingError(HTTPException):
  def __init__(self, detail: str = "Error processing order"):
    super().__init__(status_code=400,detail=detail)

async def order_exception_handler(request:Request, exc: OrderProcessingError):
  error_response = ErrorResponse(
    error="Order processing failed",
    detail=exc.detail,
  )
  return JSONResponse(
    status_code=exc.status_code,
    content= error_response.dict()
  )