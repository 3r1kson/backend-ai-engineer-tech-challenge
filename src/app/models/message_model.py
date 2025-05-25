# python
from pydantic import BaseModel
from datetime import datetime

class MessageModel(BaseModel):
    sender: str
    content: str
    timestamp: datetime