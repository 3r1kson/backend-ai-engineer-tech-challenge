# python
from pydantic import BaseModel
from typing import List, Optional

# app
from src.app.models.message_model import MessageModel

class ConversationContext(BaseModel):
    history: List[MessageModel]
    prospect_id: Optional[str]



