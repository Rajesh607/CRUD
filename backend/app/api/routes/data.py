import os
import uuid
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import settings
from app.db.session import get_db
from app.engines.pattern_engine import PatternEngine
from app.models.models import (
    Company,
    CompanySummary,
    ExtractedData,
    NormalizationPattern,
    NormalizationRule,
    Upload,
    User,
)
from app.schemas.company import CompanyOut, CompanySummaryOut, UploadOut
from app.services.ai_service import AIService
from app.utils.file_parser import detect_file_type, extract_content, validate_file_type

router = APIRouter(tags=["data"])
ai_service = AIService()
os.makedirs(settings.upload_dir, exist_ok=True)


@router.post("/upload", response_model=CompanyOut)
async def upload_company_data(
    company_type: str = Form(...),
    input_text: str | None = Form(default=None),
    file: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if company_type not in {"company_a", "target_company"}:
        raise HTTPException(status_code=400, detail="company_type must be company_a or target_company")

    if not file and not input_text:
        raise HTTPException(status_code=400, detail="Either file or input_text is required")

    filename = "manual-input.txt"
    file_ext = ".txt"
    file_path = ""
    file_size = len(input_text.encode("utf-8")) if input_text else 0
    raw_text = input_text or ""
    metadata = {"source": "copy_paste"}

    if file:
        file_ext = detect_file_type(file.filename)
        if not validate_file_type(file_ext):
            raise HTTPException(status_code=400, detail="Unsupported file type")

        content = await file.read()
        file_size = len(content)
        if file_size > settings.max_upload_size_mb * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File size exceeds 25 MB")

        filename = file.filename
        stored_name = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(settings.upload_dir, stored_name)
        with open(file_path, "wb") as f:
            f.write(content)

        raw_text, metadata = extract_content(file_path, file_ext)

    upload = Upload(
        user_id=current_user.id,
        company_type=company_type,
        filename=filename,
        file_type=file_ext,
        file_path=file_path,
        file_size=file_size,
        status="processed",
    )
    db.add(upload)
    db.commit()
    db.refresh(upload)

    extracted = ExtractedData(
        user_id=current_user.id,
        upload_id=upload.id,
        raw_text=raw_text,
        structured_data={},
        metadata=metadata,
    )
    db.add(extracted)

    signature = PatternEngine.generate_signature(raw_text)
    pattern, rule = PatternEngine.find_known_pattern(db, signature)

    if pattern and rule:
        normalized = PatternEngine.apply_rule_based_normalization(raw_text, rule.mapping_logic)
        normalized_by = "rule"
    else:
        normalized = ai_service.normalize_unknown_pattern(raw_text)
        normalized_by = "ai"
        pattern = NormalizationPattern(
            user_id=current_user.id,
            signature=signature,
            description="Auto-learned pattern from unknown input",
        )
        db.add(pattern)
        db.flush()

        new_rule = NormalizationRule(
            user_id=current_user.id,
            pattern_id=pattern.id,
            mapping_logic=normalized,
        )
        db.add(new_rule)

    company = Company(
        user_id=current_user.id,
        upload_id=upload.id,
        company_type=company_type,
        normalized_by=normalized_by,
        **normalized,
    )
    db.add(company)
    db.flush()

    summary_data = ai_service.summarize_company(normalized)
    summary = CompanySummary(user_id=current_user.id, company_id=company.id, **summary_data)
    db.add(summary)

    db.commit()
    db.refresh(company)
    return company


@router.get("/uploads", response_model=list[UploadOut])
def list_uploads(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return (
        db.query(Upload)
        .filter(Upload.user_id == current_user.id)
        .order_by(Upload.created_at.desc())
        .all()
    )


@router.get("/company/{company_id}", response_model=CompanyOut)
def get_company(company_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    company = db.query(Company).filter(Company.id == company_id, Company.user_id == current_user.id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.get("/summary/{company_id}", response_model=CompanySummaryOut)
def get_summary(company_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    summary = (
        db.query(CompanySummary)
        .filter(CompanySummary.company_id == company_id, CompanySummary.user_id == current_user.id)
        .first()
    )
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary
