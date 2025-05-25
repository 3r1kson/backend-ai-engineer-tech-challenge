# python
from pydantic import BaseModel
from typing import List

class AnalysisResult(BaseModel):
    intent: str
    entities: List[str]
    sentiment: str