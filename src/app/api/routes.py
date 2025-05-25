# python
from fastapi import APIRouter

# app
from src.app.models.process_message_request import ProcessMessageRequest
from src.app.models.process_message_response import ProcessMessageResponse
from src.app.services.message_service import process_incoming_message

router = APIRouter()

@router.get("/")
async def teste():
    return {"message": "Hello world"}

@router.post("/process_message", response_model=ProcessMessageResponse)
async def process_message(request_data: ProcessMessageRequest):
    return process_incoming_message(request_data)