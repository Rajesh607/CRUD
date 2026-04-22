import os
import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.deps import get_current_user
from app.models import Company, CompanySummary, ExtractedData, NormalizationPattern, NormalizationRule, Upload, User
from app.services.ai_service import AIService
from app.services.file_service import detect_extension, extract_file, validate_file
from app.services.pattern_service import PatternService

router = APIRouter(tags=["data"])
os.makedirs(settings.upload_dir, exist_ok=True)
ai = AIService()


@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "role": current_user.role}


@router.post("/upload")
async def upload(
    company_type: str = Form(...),
    input_text: str | None = Form(None),
    source_type: str = Form("file"),
    file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if company_type not in {"company_a", "target_company"}:
        raise HTTPException(status_code=400, detail="Invalid company_type")

    raw_text = input_text or ""
    metadata = {"source": source_type}
    file_path = ""
    file_name = "manual-input"
    file_type = "text"
    file_size = len(raw_text.encode())

    if file:
        data = await file.read()
        ext = detect_extension(file.filename)
        try:
            validate_file(ext, len(data), settings.max_upload_mb)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        file_name = file.filename
        file_type = ext
        file_size = len(data)
        stored = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(settings.upload_dir, stored)
        with open(file_path, "wb") as out:
            out.write(data)

        raw_text, metadata = extract_file(file_path, ext)

    upload_rec = Upload(
        user_id=current_user.id,
        company_type=company_type,
        source_type=source_type,
        filename=file_name,
        file_type=file_type,
        file_path=file_path,
        file_size=file_size,
        status="processed",
    )
    db.add(upload_rec)
    db.flush()

    extracted = ExtractedData(
        user_id=current_user.id,
        upload_id=upload_rec.id,
        raw_text=raw_text,
        structured_data={},
        extraction_metadata=metadata,
    )
    db.add(extracted)

    signature = PatternService.signature(raw_text)
    known_rule = PatternService.get_known_rule(db, signature)

    if known_rule:
        normalized = PatternService.apply_rule(raw_text, known_rule.mapping_logic)
        normalized_by = "rule"
    else:
        normalized = ai.normalize_unknown_pattern(raw_text)
        normalized_by = "ai"
        pattern = NormalizationPattern(user_id=current_user.id, signature=signature, description="Learned from unknown input")
        db.add(pattern)
        db.flush()
        db.add(NormalizationRule(user_id=current_user.id, pattern_id=pattern.id, mapping_logic=normalized))

    company = Company(user_id=current_user.id, upload_id=upload_rec.id, company_type=company_type, normalized_by=normalized_by, **normalized)
    db.add(company)
    db.flush()

    summary_payload = ai.summarize_company(normalized)
    db.add(CompanySummary(user_id=current_user.id, company_id=company.id, **summary_payload))

    db.commit()
    return {"company_id": company.id, "normalized_by": normalized_by, "pattern_signature": signature}


@router.get("/uploads")
def uploads(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rows = db.query(Upload).filter_by(user_id=current_user.id).order_by(Upload.id.desc()).all()
    return rows


@router.get("/company/{company_id}")
def company(company_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    row = db.query(Company).filter_by(user_id=current_user.id, id=company_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    return row


@router.get("/summary/{company_id}")
def summary(company_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    row = db.query(CompanySummary).filter_by(user_id=current_user.id, company_id=company_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    return row
