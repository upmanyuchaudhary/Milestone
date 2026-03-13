from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.schemas import HoldingResponse, HoldingCreate
from backend import models

router = APIRouter()


@router.get("/holdings", response_model=List[HoldingResponse])
def get_holdings(db: Session = Depends(get_db)):
    """All active holdings with their latest scores."""
    from backend.services.portfolio_service import get_all_holdings
    return get_all_holdings(db)


@router.get("/holdings/{holding_id}", response_model=HoldingResponse)
def get_holding(holding_id: int, db: Session = Depends(get_db)):
    """Single holding with full score breakdown and history."""
    from backend.services.portfolio_service import get_holding_detail
    holding = get_holding_detail(db, holding_id)
    if not holding:
        raise HTTPException(status_code=404, detail="Holding not found")
    return holding


@router.post("/holdings", response_model=HoldingResponse, status_code=201)
def add_holding(payload: HoldingCreate, db: Session = Depends(get_db)):
    """Add a new holding with Cat A/B/C assignment."""
    from backend.services.portfolio_service import create_holding
    return create_holding(db, payload)


@router.get("/summary")
def get_portfolio_summary(db: Session = Depends(get_db)):
    """Portfolio totals: total value, P&L, overall health, allocation."""
    from backend.services.portfolio_service import get_summary
    return get_summary(db)


@router.get("/allocation")
def get_allocation(db: Session = Depends(get_db)):
    """Allocation breakdown — each stock as % of total portfolio."""
    from backend.services.portfolio_service import get_allocation_breakdown
    return get_allocation_breakdown(db)
