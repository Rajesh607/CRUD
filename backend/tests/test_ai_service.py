from app.services.ai_service import AIService


def test_mock_summary_contains_overview():
    service = AIService()
    company = {"company_name": "Acme", "industry": "FinTech", "country": "US", "revenue": "$1M", "risks": []}
    result = service.summarize_company(company)
    assert "overview" in result
    assert result["key_insights"]
