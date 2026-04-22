from datetime import datetime
from pydantic import BaseModel


class UploadOut(BaseModel):
    id: int
    filename: str
    file_type: str
    status: str
    company_type: str
    created_at: datetime

    class Config:
        from_attributes = True


class CompanyOut(BaseModel):
    id: int
    company_name: str
    industry: str
    country: str
    revenue: str
    employees: str
    website: str
    executives: list
    products_services: list
    partners: list
    risks: list
    source_facts: list
    normalized_by: str

    class Config:
        from_attributes = True


class CompanySummaryOut(BaseModel):
    company_id: int
    overview: str
    key_insights: list
    risks: list
    important_facts: list


class AnalyzeRequest(BaseModel):
    company_a_id: int
    target_company_id: int


class RelationshipOut(BaseModel):
    id: int
    company_a_id: int
    target_company_id: int
    links: list
    similarities: list
    risks: list
    opportunities: list
    similarity_score: float
    risk_score: float
    opportunity_score: float
    confidence_score: float
    ai_summary: str

    class Config:
        from_attributes = True
