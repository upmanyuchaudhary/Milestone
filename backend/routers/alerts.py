from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/active")
def get_active_alerts(db: Session = Depends(lambda: next(__import__('database').get_db()))):
    from services.alerts_service import get_active
    return get_active(db)


@router.post("/{alert_id}/action")
def respond_to_alert(alert_id: int, payload: dict, db: Session = Depends(lambda: next(__import__('database').get_db()))):
    from services.alerts_service import record_action
    result = record_action(db, alert_id, payload.get("action"))
    if not result:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"status": "ok", "action": payload.get("action")}


@router.get("/history")
def get_alert_history(db: Session = Depends(lambda: next(__import__('database').get_db()))):
    from services.alerts_service import get_history
    return get_history(db)


@router.get("/accuracy")
def get_accuracy(db: Session = Depends(lambda: next(__import__('database').get_db()))):
    from services.alerts_service import get_accuracy_log
    return get_accuracy_log(db)