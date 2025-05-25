# python
from typing import Union, List

from pydantic import BaseModel, root_validator
from datetime import datetime

class MessageModel(BaseModel):
    sender: str
    content: Union[str, List[str]]
    timestamp: datetime

    @root_validator(pre=True)
    def join_content_list(cls, values):
        content = values.get("content")
        if isinstance(content, list):
            values["content"] = " ".join(content)
        return values