# python
import json
import logging
from typing import Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# app
from src.app.tools.crm_tool import fetch_prospect_details
from src.app.tools.rag_tool import query_knowledge_base
from src.config.config import get_open_ai_key

logger = logging.getLogger(__name__)

class LLMHandler:
    def __init__(self):
        self.llm = ChatOpenAI(openai_api_key=get_open_ai_key(), temperature=0)
        self.tool_discovery_prompt = PromptTemplate(
            input_variables=["context", "message"],
            template="""
            You are an expert AI sales assistant. Given the context and new message:
            1. Classify intent, sentiment, and entities.
            2. Decide if you require CRM data or knowledge base info.
            3. Return JSON with 'tool_calls' specifying needed data fields or queries.

            Return only JSON like this:
            {{
              "tool_calls": {{
                "crm": {{"required": true|false, "fields": ["..."]}},
                "knowledge_base": {{"required": true|false, "query": "..."}}
              }},
              "classification": {{"intent": "...", "sentiment": "...", "entities": ["..."]}}
            }}

            Context:
            {context}

            New Message:
            {message}
            """
        )
        self.tool_discovery_chain = LLMChain(llm=self.llm, prompt=self.tool_discovery_prompt)

        self.final_response_prompt = PromptTemplate(
            input_variables=["context", "message", "crm_data", "kb_data"],
            template="""
                    You are an expert AI sales assistant. Using the context, new message, CRM data, and knowledge base data, generate:
                    1. A confident, helpful response.
                    2. The intended action.
                    3. Classification of intent, sentiment, entities, and priority.
                    4. Confidence score and reasoning trace.

                    Return this as strict JSON with fields:
                    {{
                      "response": "...",
                      "action": "...",
                      "classification": {{
                        "intent": "...",
                        "sentiment": "...",
                        "entities": ["...", "..."],
                        "priority": "low|medium|high"
                      }},
                      "confidence_score": 0.0-1.0,
                      "reasoning_trace": "..."
                    }}

                    Context:
                    {context}

                    New Message:
                    {message}

                    CRM Data:
                    {crm_data}

                    Knowledge Base Data:
                    {kb_data}
                    """
        )
        self.final_response_chain = LLMChain(llm=self.llm, prompt=self.final_response_prompt)

    def analyze(self, context: str, message: str, prospect_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            tool_discovery_raw = self.tool_discovery_chain.run(context=context, message=message)
            tool_discovery_output = json.loads(tool_discovery_raw)
        except Exception as e:
            logger.error(f"Error during tool discovery or parsing JSON: {e}")
            tool_discovery_output = {
                "tool_calls": {"crm": {"required": False}, "knowledge_base": {"required": False}},
                "classification": {"intent": "unknown", "sentiment": "neutral", "entities": []}
            }

        tool_calls = tool_discovery_output.get("tool_calls", {})
        crm_data = None
        kb_data = None
        tool_usage_log = []

        if tool_calls.get("crm", {}).get("required") and prospect_id:
            crm_fields = tool_calls["crm"].get("fields", [])
            full_data = fetch_prospect_details(prospect_id)
            crm_data = {k: full_data.get(k) for k in crm_fields} if crm_fields else full_data
            tool_usage_log.append({
                "tool": "CRM",
                "input": {"prospect_id": prospect_id, "fields": crm_fields},
                "output": crm_data
            })

        if tool_calls.get("knowledge_base", {}).get("required"):
            query = tool_calls["knowledge_base"].get("query", "")
            if query:
                kb_data = query_knowledge_base(query)
                tool_usage_log.append({
                    "tool": "KnowledgeBase",
                    "input": {"query": query},
                    "output": kb_data
                })

        crm_data_str = json.dumps(crm_data, indent=2) if crm_data else "None"
        kb_data_str = json.dumps(kb_data, indent=2) if kb_data else "None"

        try:
            final_response_raw = self.final_response_chain.run(
                context=context,
                message=message,
                crm_data=crm_data_str,
                kb_data=kb_data_str
            )
            final_response_output = json.loads(final_response_raw)
        except Exception as e:
            logger.error(f"Error during final response or parsing JSON: {e}")
            final_response_output = {
                "response": "Sorry, I could not process your request.",
                "action": None,
                "classification": {"intent": "unknown", "sentiment": "neutral", "entities": [], "priority": "low"},
                "confidence_score": 0.0,
                "reasoning_trace": "Failed to parse final LLM output"
            }

        final_response_output.update({
            "tool_calls": tool_calls,
            "tool_usage_log": tool_usage_log,
            "crm_data": crm_data,
            "knowledge_base_results": kb_data
        })

        return final_response_output
