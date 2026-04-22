from app.services.ai_service import AIService


def test_normalize_unknown_pattern_returns_dict():
    service = AIService()
    payload = service.normalize_unknown_pattern("Company Name: X")
    assert isinstance(payload, dict)
    assert "company_name" in payload
