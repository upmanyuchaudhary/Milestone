from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/dashboard")
def get_home_dashboard(db: Session = Depends(lambda: next(__import__('database').get_db()))):
    from services.home_service import build_dashboard
    return build_dashboard(db)