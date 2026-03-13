from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()


@router.get("/progress")
def get_milestone_progress(db: Session = Depends(lambda: next(__import__('database').get_db()))):
    from services.milestone_service import get_progress
    return get_progress(db)


@router.get("/history")
def get_milestone_history(db: Session = Depends(lambda: next(__import__('database').get_db()))):
    from services.milestone_service import get_history
    return get_history(db)


@router.get("/contributions")
def get_contributions(db: Session = Depends(lambda: next(__import__('database').get_db()))):
    from services.milestone_service import get_contribution_breakdown
    return get_contribution_breakdown(db)


@router.post("/scenario")
def run_scenario(payload: dict, db: Session = Depends(lambda: next(__import__('database').get_db()))):
    from services.milestone_service import compute_scenario
    return compute_scenario(db, payload)


@router.put("/config")
def update_config(payload: dict, db: Session = Depends(lambda: next(__import__('database').get_db()))):
    from services.milestone_service import update_milestone_config
    return update_milestone_config(db, payload)