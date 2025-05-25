# python
from pydantic import BaseModel
from typing import List, Dict, Optional, Any


class ActionableOutput(BaseModel):
    suggested_response_draft: str
    internal_next_steps: List[Dict[str, Any]]
    tool_usage_log: List[Dict] = None
    confidence_score: float | None = None
    reasoning_trace: str | None = None

    classification: Optional[Dict[str, Any]] = None
    crm_data: Optional[Dict[str, Any]] = None
    knowledge_base_results: Optional[Any] = None