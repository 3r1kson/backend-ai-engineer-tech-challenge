# python
import logging
from typing import Dict

CRM_DATA = {
    "prospect_001": {
        "name": "Jackie Chan",
        "company": "TechCorp",
        "lead_score": 85,
        "company_size": "Medium",
        "technologies_used": ["AWS", "Docker", "Kubernetes"]
    },
    "prospect_002": {
        "name": "Jiraya",
        "company": "NinjasCorp",
        "lead_score": 85,
        "company_size": "Medium",
        "technologies_used": ["AWS", "Docker", "Kubernetes"]
    },
}

logger = logging.getLogger(__name__)

def fetch_prospect_details(prospect_id: str) -> Dict:
    details = CRM_DATA.get(prospect_id, {})
    if details:
        logger.info(f"Fetched CRM data for prospect_id: {prospect_id}")
    else:
        logger.warning(f"No CRM data found for prospect_id: {prospect_id}")
    return details

