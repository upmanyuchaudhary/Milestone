from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.schemas import AlertResponse, AlertActionRequest, AccuracyResponse

router = APIRouter()


@router.get("/active", response_model=List[AlertResponse])
def get_active_alerts(db: Session = Depends(get_db)):
    """All active recommendations sorted by milestone impact (highest first)."""
    from backend.services.alerts_service import get_active
    return get_active(db)


@router.post("/{alert_id}/action")
def respond_to_alert(
    alert_id: int,
    payload: AlertActionRequest,
    db: Session = Depends(get_db)
):
    """User responds to a recommendation — ACTED, IGNORED, or WATCHING."""
    from backend.services.alerts_service import record_action
    result = record_action(db, alert_id, payload.action)
    if not result:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"status": "ok", "action": payload.action}


@router.get("/history")
def get_alert_history(db: Session = Depends(get_db)):
    """Last 10 recommendations with their outcomes."""
    from backend.services.alerts_service import get_history
    return get_history(db)


@router.get("/ignored")
def get_ignored_alerts(db: Session = Depends(get_db)):
    """Ignored alerts with the financial cost of ignoring."""
    from backend.services.alerts_service import get_ignored
    return get_ignored(db)


@router.get("/accuracy", response_model=List[AccuracyResponse])
def get_accuracy(db: Session = Depends(get_db)):
    """Monthly signal accuracy scorecard."""
    from backend.services.alerts_service import get_accuracy_log
    return get_accuracy_log(db)
