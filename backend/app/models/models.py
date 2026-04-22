from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), default="analyst")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Upload(Base):
    __tablename__ = "uploads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    company_type: Mapped[str] = mapped_column(String(50))
    filename: Mapped[str] = mapped_column(String(255))
    file_type: Mapped[str] = mapped_column(String(50))
    file_path: Mapped[str] = mapped_column(String(512))
    file_size: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(50), default="uploaded")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ExtractedData(Base):
    __tablename__ = "extracted_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    upload_id: Mapped[int] = mapped_column(ForeignKey("uploads.id"), index=True)
    raw_text: Mapped[str] = mapped_column(Text)
    structured_data: Mapped[dict] = mapped_column(JSON, default={})
    metadata: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class NormalizationPattern(Base):
    __tablename__ = "normalization_patterns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    signature: Mapped[str] = mapped_column(String(255), index=True, unique=True)
    description: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class NormalizationRule(Base):
    __tablename__ = "normalization_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    pattern_id: Mapped[int] = mapped_column(ForeignKey("normalization_patterns.id"), index=True)
    mapping_logic: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    upload_id: Mapped[int] = mapped_column(ForeignKey("uploads.id"), index=True)
    company_type: Mapped[str] = mapped_column(String(50))
    company_name: Mapped[str] = mapped_column(String(255), index=True)
    industry: Mapped[str] = mapped_column(String(100), default="")
    country: Mapped[str] = mapped_column(String(100), default="")
    revenue: Mapped[str] = mapped_column(String(100), default="")
    employees: Mapped[str] = mapped_column(String(100), default="")
    website: Mapped[str] = mapped_column(String(255), default="")
    executives: Mapped[dict] = mapped_column(JSON, default=[])
    products_services: Mapped[dict] = mapped_column(JSON, default=[])
    partners: Mapped[dict] = mapped_column(JSON, default=[])
    risks: Mapped[dict] = mapped_column(JSON, default=[])
    source_facts: Mapped[dict] = mapped_column(JSON, default=[])
    normalized_by: Mapped[str] = mapped_column(String(50), default="rule")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CompanySummary(Base):
    __tablename__ = "company_summaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    overview: Mapped[str] = mapped_column(Text)
    key_insights: Mapped[dict] = mapped_column(JSON, default=[])
    risks: Mapped[dict] = mapped_column(JSON, default=[])
    important_facts: Mapped[dict] = mapped_column(JSON, default=[])
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class RelationshipAnalysis(Base):
    __tablename__ = "relationship_analysis"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    company_a_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    target_company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    links: Mapped[dict] = mapped_column(JSON, default=[])
    similarities: Mapped[dict] = mapped_column(JSON, default=[])
    risks: Mapped[dict] = mapped_column(JSON, default=[])
    opportunities: Mapped[dict] = mapped_column(JSON, default=[])
    similarity_score: Mapped[float] = mapped_column(Float, default=0.0)
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    opportunity_score: Mapped[float] = mapped_column(Float, default=0.0)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0)
    ai_summary: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
