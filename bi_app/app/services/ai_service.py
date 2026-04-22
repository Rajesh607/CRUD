import os


class AIService:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.mock_mode = not bool(self.api_key)

    def normalize_unknown_pattern(self, raw_text: str) -> dict:
        if self.mock_mode:
            return {
                "company_name": "Unknown Company",
                "industry": "Unknown",
                "country": "Unknown",
                "revenue": "N/A",
                "employees": "N/A",
                "website": "",
                "executives": [],
                "products_services": [],
                "partners": [],
                "risks": ["Insufficient source data"],
                "source_facts": [raw_text[:300]],
            }
        # Plug in provider SDK call here; fallback placeholder until wired.
        return {
            "company_name": "AI Normalized Company",
            "industry": "Technology",
            "country": "US",
            "revenue": "Unknown",
            "employees": "Unknown",
            "website": "",
            "executives": [],
            "products_services": [],
            "partners": [],
            "risks": ["AI inference confidence required"],
            "source_facts": [raw_text[:300]],
        }

    def summarize_company(self, company: dict) -> dict:
        return {
            "overview": f"{company.get('company_name', 'Company')} operates in {company.get('industry', 'unknown industry')}",
            "key_insights": [
                f"Country: {company.get('country', 'N/A')}",
                f"Revenue: {company.get('revenue', 'N/A')}",
            ],
            "risks": company.get("risks", []) or ["Low public visibility"],
            "important_facts": company.get("source_facts", [])[:3],
        }

    def analyze_relationship(self, company_a: dict, company_b: dict) -> dict:
        same_industry = company_a.get("industry") == company_b.get("industry")
        same_country = company_a.get("country") == company_b.get("country")
        similarity = 0.4 + (0.35 if same_industry else 0) + (0.15 if same_country else 0)
        return {
            "links": list(set(company_a.get("partners", [])).intersection(company_b.get("partners", []))),
            "similarities": [s for s in ["Same industry" if same_industry else None, "Same country" if same_country else None] if s],
            "risks": ["Portfolio concentration risk"],
            "opportunities": ["Cross-sell and partnership opportunities"],
            "similarity_score": round(min(similarity, 1.0), 2),
            "risk_score": 0.42,
            "opportunity_score": 0.71,
            "confidence_score": 0.66,
            "ai_summary": "The two companies have moderate strategic fit with manageable overlap risk.",
        }
