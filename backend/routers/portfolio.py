from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
router = APIRouter()

@router.get("/holdings")
def get_holdings(db: Session = Depends(lambda: next(__import__('database').get_db()))):
    from services.portfolio_service import get_all_holdings
    return get_all_holdings(db)

@router.get("/holdings/{holding_id}")
def get_holding(holding_id: int, db: Session = Depends(lambda: next(__import__('database').get_db()))):
    from services.portfolio_service import get_holding_detail
    holding = get_holding_detail(db, holding_id)
    if not holding:
        raise HTTPException(status_code=404, detail="Holding not found")
    return holding

@router.post("/holdings", status_code=201)
def add_holding(payload: dict, db: Session = Depends(lambda: next(__import__('database').get_db()))):
    from services.portfolio_service import create_holding
    return create_holding(db, payload)

@router.get("/summary")
def get_portfolio_summary(db: Session = Depends(lambda: next(__import__('database').get_db()))):
    from services.portfolio_service import get_summary
    return get_summary(db)

@router.get("/allocation")
def get_allocation(db: Session = Depends(lambda: next(__import__('database').get_db()))):
    from services.portfolio_service import get_allocation_breakdown
    return get_allocation_breakdown(db)

@router.post("/sync")
def sync_holdings(db: Session = Depends(lambda: next(__import__('database').get_db()))):
    from services.kite_service import fetch_holdings
    from services.portfolio_service import sync_holdings_to_db
    holdings = fetch_holdings()
    result = sync_holdings_to_db(db, holdings)
    return result