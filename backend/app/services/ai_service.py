import os


class AIService:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.mock_mode = not self.api_key

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
                "risks": ["Insufficient data"],
                "source_facts": [raw_text[:300]],
            }
        # Placeholder for real provider call
        return self.normalize_unknown_pattern(raw_text)

    def summarize_company(self, company: dict) -> dict:
        return {
            "overview": f"{company.get('company_name')} operates in {company.get('industry')}.",
            "key_insights": [
                f"Located in {company.get('country', 'N/A')}",
                f"Revenue stated as {company.get('revenue', 'N/A')}",
            ],
            "risks": company.get("risks", []) or ["Limited disclosures"],
            "important_facts": company.get("source_facts", [])[:3],
        }

    def analyze_relationship(self, company_a: dict, target: dict) -> dict:
        similar_industry = company_a.get("industry") == target.get("industry")
        similar_country = company_a.get("country") == target.get("country")

        similarity = 0.7 if similar_industry else 0.4
        if similar_country:
            similarity += 0.2

        return {
            "links": list(set(company_a.get("partners", [])).intersection(set(target.get("partners", [])))),
            "similarities": [
                s
                for s in [
                    "Same industry" if similar_industry else None,
                    "Same country" if similar_country else None,
                ]
                if s
            ],
            "risks": ["Potential market overlap risk"],
            "opportunities": ["Potential strategic alliance"],
            "similarity_score": min(similarity, 1.0),
            "risk_score": 0.45,
            "opportunity_score": 0.72,
            "confidence_score": 0.68,
            "ai_summary": "The companies appear moderately aligned with potential partnership opportunities.",
        }
