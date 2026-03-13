from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.schemas import (
    MilestoneProgress, MilestoneHistoryItem,
    ScenarioRequest, ScenarioResponse, MilestoneConfigUpdate
)

router = APIRouter()


@router.get("/progress", response_model=MilestoneProgress)
def get_milestone_progress(db: Session = Depends(get_db)):
    """Current milestone status — value, %, projected date, days ahead/behind."""
    from backend.services.milestone_service import get_progress
    return get_progress(db)


@router.get("/history", response_model=List[MilestoneHistoryItem])
def get_milestone_history(db: Session = Depends(get_db)):
    """Month by month history since start."""
    from backend.services.milestone_service import get_history
    return get_history(db)


@router.get("/contributions")
def get_contributions(db: Session = Depends(get_db)):
    """How the milestone is being built — equity/SIP/rebalancing breakdown."""
    from backend.services.milestone_service import get_contribution_breakdown
    return get_contribution_breakdown(db)


@router.post("/scenario", response_model=ScenarioResponse)
def run_scenario(payload: ScenarioRequest, db: Session = Depends(get_db)):
    """What-if calculation — adjust SIP, target, or date and see impact."""
    from backend.services.milestone_service import compute_scenario
    return compute_scenario(db, payload)


@router.put("/config")
def update_config(payload: MilestoneConfigUpdate, db: Session = Depends(get_db)):
    """Update milestone goal, SIP amount, or target date."""
    from backend.services.milestone_service import update_milestone_config
    return update_milestone_config(db, payload)
