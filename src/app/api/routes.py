# python
from fastapi import APIRouter

# app
from src.app.models.process_message_request_model import ProcessMessageRequestModel
from src.app.models.process_message_response_model import ProcessMessageResponseModel
from src.app.services.message_service import process_incoming_message

router = APIRouter()

@router.get("/")
async def teste():
    return {"message": "Hello world"}

@router.post("/process_message", response_model=ProcessMessageResponseModel)
async def process_message(request_data: ProcessMessageRequestModel):
    return process_incoming_message(request_data)