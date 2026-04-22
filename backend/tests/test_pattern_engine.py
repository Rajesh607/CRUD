from app.engines.pattern_engine import PatternEngine


def test_generate_signature_is_stable():
    text = "Company Name: Acme\nIndustry: SaaS\nCountry: US"
    sig1 = PatternEngine.generate_signature(text)
    sig2 = PatternEngine.generate_signature(text)
    assert sig1 == sig2
    assert len(sig1) == 32
