# python
from pydantic import BaseModel
from typing import List, Optional, Dict

class ProcessMessageResponse(BaseModel):
    response_text: str
    action: Optional[str] = None
    classification: Dict[str, str]
    knowledge_base_results: Optional[List[str]] = None
    crm_data: Optional[Dict] = None
    tool_usage_log: Optional[List[Dict]] = None
    confidence_score: Optional[float] = None
    reasoning_trace: Optional[str] = None