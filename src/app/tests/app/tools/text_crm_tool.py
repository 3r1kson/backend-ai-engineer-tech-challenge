# app
from src.app.tools.crm_tool import fetch_prospect_details

def test_fetch_prospect_details_found():
    data = fetch_prospect_details("prospect_001")
    assert data.get("name") == "Jackie Chan"
    assert "lead_score" in data
    print(f"Data: {data}")

def test_fetch_prospect_details_not_found():
    data = fetch_prospect_details("unknown_id")
    assert data == {}