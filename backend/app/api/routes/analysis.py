from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.models import Company, RelationshipAnalysis, User
from app.schemas.company import AnalyzeRequest, RelationshipOut
from app.services.ai_service import AIService

router = APIRouter(tags=["analysis"])
ai_service = AIService()


@router.post("/analyze", response_model=RelationshipOut)
def analyze_companies(
    payload: AnalyzeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    company_a = db.query(Company).filter(Company.id == payload.company_a_id, Company.user_id == current_user.id).first()
    target = (
        db.query(Company)
        .filter(Company.id == payload.target_company_id, Company.user_id == current_user.id)
        .first()
    )

    if not company_a or not target:
        raise HTTPException(status_code=404, detail="Company record not found")

    analysis_data = ai_service.analyze_relationship(company_a.__dict__, target.__dict__)
    analysis = RelationshipAnalysis(
        user_id=current_user.id,
        company_a_id=company_a.id,
        target_company_id=target.id,
        **analysis_data,
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis


@router.get("/relationship/{analysis_id}", response_model=RelationshipOut)
def get_relationship(analysis_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    analysis = (
        db.query(RelationshipAnalysis)
        .filter(RelationshipAnalysis.id == analysis_id, RelationshipAnalysis.user_id == current_user.id)
        .first()
    )
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis
