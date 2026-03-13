from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas import HomeDashboard

router = APIRouter()


@router.get("/dashboard", response_model=HomeDashboard)
def get_home_dashboard(db: Session = Depends(get_db)):
    """
    Returns everything Screen 1 needs in a single API call.
    Reads from DB — does not call Kite API directly.
    """
    from backend.services.home_service import build_dashboard
    return build_dashboard(db)
