import hashlib
import re
from sqlalchemy.orm import Session

from app.models.models import NormalizationPattern, NormalizationRule


class PatternEngine:
    @staticmethod
    def generate_signature(raw_text: str) -> str:
        tokens = re.findall(r"[A-Za-z_]+", raw_text.lower())
        header_tokens = sorted(list(set(tokens[:40])))
        payload = "|".join(header_tokens)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:32]

    @staticmethod
    def find_known_pattern(db: Session, signature: str) -> tuple[NormalizationPattern | None, NormalizationRule | None]:
        pattern = db.query(NormalizationPattern).filter(NormalizationPattern.signature == signature).first()
        if not pattern:
            return None, None
        rule = db.query(NormalizationRule).filter(NormalizationRule.pattern_id == pattern.id).first()
        return pattern, rule

    @staticmethod
    def apply_rule_based_normalization(raw_text: str, mapping_logic: dict) -> dict:
        normalized = {
            "company_name": mapping_logic.get("company_name", "Unknown Company"),
            "industry": mapping_logic.get("industry", "Unknown"),
            "country": mapping_logic.get("country", "Unknown"),
            "revenue": mapping_logic.get("revenue", "N/A"),
            "employees": mapping_logic.get("employees", "N/A"),
            "website": mapping_logic.get("website", ""),
            "executives": mapping_logic.get("executives", []),
            "products_services": mapping_logic.get("products_services", []),
            "partners": mapping_logic.get("partners", []),
            "risks": mapping_logic.get("risks", []),
            "source_facts": [raw_text[:300]],
        }
        return normalized
