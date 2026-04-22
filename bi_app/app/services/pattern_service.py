import hashlib
import re

from sqlalchemy.orm import Session

from app.models import NormalizationPattern, NormalizationRule


class PatternService:
    @staticmethod
    def signature(raw_text: str) -> str:
        tokens = re.findall(r"[A-Za-z_]+", raw_text.lower())
        seed = "|".join(sorted(set(tokens[:50])))
        return hashlib.sha256(seed.encode()).hexdigest()[:40]

    @staticmethod
    def get_known_rule(db: Session, signature: str) -> NormalizationRule | None:
        pattern = db.query(NormalizationPattern).filter_by(signature=signature).first()
        if not pattern:
            return None
        return db.query(NormalizationRule).filter_by(pattern_id=pattern.id).first()

    @staticmethod
    def apply_rule(raw_text: str, mapping: dict) -> dict:
        baseline = {
            "company_name": mapping.get("company_name", "Unknown"),
            "industry": mapping.get("industry", "Unknown"),
            "country": mapping.get("country", "Unknown"),
            "revenue": mapping.get("revenue", "N/A"),
            "employees": mapping.get("employees", "N/A"),
            "website": mapping.get("website", ""),
            "executives": mapping.get("executives", []),
            "products_services": mapping.get("products_services", []),
            "partners": mapping.get("partners", []),
            "risks": mapping.get("risks", []),
            "source_facts": mapping.get("source_facts", [raw_text[:300]]),
        }
        return baseline
