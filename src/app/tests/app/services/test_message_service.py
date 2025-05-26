# python
from datetime import datetime
import json

# app
from src.app.services.message_service import process_incoming_message
from src.app.models.process_message_request_model import ProcessMessageRequestModel
from src.app.models.message_model import MessageModel

def test_process_message_with_tools():
    request = ProcessMessageRequestModel(
        conversation_history=[
            MessageModel(sender="prospect", content="I'm interested in your product.", timestamp=datetime.now())
        ],
        current_prospect_message="Can you tell me more about the pricing?",
        prospect_id="prospect_001"
    )
    response = process_incoming_message(request)
    assert response.status_code == 200
    data = json.loads(response.body.decode())["data"]
    assert "knowledge_base_results" in data
    assert "crm_data" in data
    assert "tool_usage_log" in data
