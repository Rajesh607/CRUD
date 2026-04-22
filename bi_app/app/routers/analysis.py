from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.deps import get_current_user
from app.models import Company, RelationshipAnalysis, User
from app.schemas import AnalyzeIn
from app.services.ai_service import AIService

router = APIRouter(tags=["analysis"])
ai = AIService()


@router.post("/analyze")
def analyze(payload: AnalyzeIn, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    a = db.query(Company).filter_by(user_id=current_user.id, id=payload.company_a_id).first()
    b = db.query(Company).filter_by(user_id=current_user.id, id=payload.target_company_id).first()
    if not a or not b:
        raise HTTPException(status_code=404, detail="Company not found")

    result = ai.analyze_relationship(a.__dict__, b.__dict__)
    rec = RelationshipAnalysis(
        user_id=current_user.id,
        company_a_id=a.id,
        target_company_id=b.id,
        **result,
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec


@router.get("/relationship/{analysis_id}")
def relationship(analysis_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    row = db.query(RelationshipAnalysis).filter_by(id=analysis_id, user_id=current_user.id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return row
