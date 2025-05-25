from typing import Optional

from src.app.llm.llm_handler import LLMHandler
from src.app.models.actionable_output_model import ActionableOutput
from src.app.models.message_model import MessageModel


class ConversationManager:
    def __init__(self):
        self.llm_handler = LLMHandler()

    def format_history(self, history: list[MessageModel]) -> str:
        return "\n".join([f"{msg.sender} ({msg.timestamp.isoformat()}): {msg.content}" for msg in history])

    def run(self, history: list[MessageModel], current_message: str, prospect_id: Optional[str] = None) -> ActionableOutput:
        context = self.format_history(history)
        llm_output = self.llm_handler.analyze(context, current_message, prospect_id)

        internal_steps = []

        if llm_output.get("crm_data"):
            internal_steps.append({
                "action": "UPDATE_CRM",
                "details": {"field": "last_engaged", "value": "now"}
            })

        if llm_output.get("knowledge_base_results"):
            internal_steps.append({
                "action": "SCHEDULE_FOLLOW_UP",
                "details": {"reason": "answered inquiry with knowledge base info"}
            })

        if llm_output.get("action") == "FLAG_FOR_HUMAN_REVIEW":
            internal_steps.append({
                "action": "FLAG_FOR_HUMAN_REVIEW",
                "details": {"reason": "complex objection or unclear response"}
            })

        return ActionableOutput(
            suggested_response_draft=llm_output.get("response", ""),
            internal_next_steps=internal_steps,
            tool_usage_log=llm_output.get("tool_usage_log", []),
            confidence_score=llm_output.get("confidence_score", 0.5),
            reasoning_trace=llm_output.get("reasoning_trace", ""),
            classification=llm_output.get("classification"),
            crm_data=llm_output.get("crm_data"),
            knowledge_base_results=llm_output.get("knowledge_base_results")
        )
