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
        self.prompt = PromptTemplate(
            input_variables=["context", "message"],
            template="""
            You are an expert AI sales assistant from Sailor AI. Analyze the context and the new message to:
            1. Classify the intent, entities, and sentiment
            2. Decide whether additional info is needed (e.g., CRM or product knowledge)
            3. Generate a confident, helpful response

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
              "reasoning_trace": "Why you responded the way you did",
              "tool_calls": {{
                "crm": {{"required": true|false, "fields": ["..."]}},
                "knowledge_base": {{"required": true|false, "query": "..."}}
              }}
            }}

            Context:
            {context}

            New Message:
            {message}
            """
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def analyze(self, context: str, message: str, prospect_id: Optional[str] = None) -> Dict[str, Any]:
        raw_response = self.chain.run(context=context, message=message)
        try:
            llm_output = json.loads(raw_response)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse LLM response as JSON: {raw_response}")
            llm_output = {
                "response": "Sorry, I could not understand the request.",
                "action": None,
                "classification": {"intent": "unknown", "sentiment": "neutral", "entities": [], "priority": "low"},
                "confidence_score": 0.0,
                "reasoning_trace": "Failed to parse LLM output JSON",
                "tool_calls": {}
            }

        tool_usage_log = []

        crm_data = None
        kb_results = None

        tool_calls = llm_output.get("tool_calls", {})

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
                kb_results = query_knowledge_base(query)
                tool_usage_log.append({
                    "tool": "KnowledgeBase",
                    "input": {"query": query},
                    "output": kb_results
                })

        result = {
            "response": llm_output.get("response", ""),
            "action": llm_output.get("action"),
            "classification": llm_output.get("classification", {}),
            "confidence_score": llm_output.get("confidence_score", 0.5),
            "reasoning_trace": llm_output.get("reasoning_trace", ""),
            "tool_usage_log": tool_usage_log,
            "crm_data": crm_data,
            "knowledge_base_results": kb_results
        }

        return result
