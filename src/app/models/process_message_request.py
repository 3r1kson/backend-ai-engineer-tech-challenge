# python
from pydantic import BaseModel
from typing import List, Optional

from src.app.models.message_model import MessageModel

class ProcessMessageRequest(BaseModel):
    conversation_history: List[MessageModel]
    current_prospect_message: str
    prospect_id: Optional[str] = None
