# python
import re

# app
from src.app.models.process_message_request import ProcessMessageRequest
from src.app.llm.llm_handler import LLMHandler
from src.app.services.conversation_manager_service import ConversationManager
from src.utils.http_responses import success_response, conflict_response, error_response, unauthorized_response, \
    bad_request_response

llm = LLMHandler()
conversationManager = ConversationManager()

def format_conversation_history(history):
    return "\n".join([f"{msg.sender} ({msg.timestamp}): {msg.content}" for msg in history])

def extract_action(response_text: str):
    match = re.search(r"ACTION:\s*(.+)", response_text)
    return match.group(1).strip() if match else None

def process_incoming_message(data: ProcessMessageRequest):
    if not data.current_prospect_message.strip():
        return bad_request_response("Current prospect message cannot be empty")

    if data.prospect_id is None:
        return unauthorized_response("Prospect ID is required")

    try:
        result = conversationManager.run(
            history=data.conversation_history,
            current_message=data.current_prospect_message,
            prospect_id=data.prospect_id
        )

        for step in result.internal_next_steps:
            if step.get("action") == "forbidden_action":
                return conflict_response("The requested action is not allowed")

        return success_response("Message processed successfully", result.dict())

    except Exception as e:
        return error_response(f"Processing error: {str(e)}", status=500)
