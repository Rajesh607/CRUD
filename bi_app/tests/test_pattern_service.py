from app.services.pattern_service import PatternService


def test_signature_deterministic():
    txt = "Company Industry Country"
    assert PatternService.signature(txt) == PatternService.signature(txt)
