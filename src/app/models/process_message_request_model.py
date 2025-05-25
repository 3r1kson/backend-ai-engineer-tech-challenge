# python
from pydantic import BaseModel
from typing import List, Optional

# app
from src.app.models.message_model import MessageModel

class ProcessMessageRequestModel(BaseModel):
    conversation_history: List[MessageModel]
    current_prospect_message: str
    prospect_id: Optional[str] = None
