"""
Portfolio service — Sprint 0 placeholder.
Returns stub data so the API is callable before Layer 1 is built.
Real implementation built in Sprint 1.
"""
from sqlalchemy.orm import Session
from backend import models
from backend.schemas import HoldingCreate


def get_all_holdings(db: Session):
    holdings = db.query(models.Holding).filter(models.Holding.is_active == True).all()
    result = []
    for h in holdings:
        result.append({
            "id": h.id,
            "tradingsymbol": h.tradingsymbol,
            "exchange": h.exchange,
            "category": h.category,
            "quantity": h.quantity,
            "average_buy_price": float(h.average_buy_price),
            "stop_loss_price": float(h.stop_loss_price) if h.stop_loss_price else None,
            "entry_date": h.entry_date,
            "is_active": h.is_active,
            "latest_scores": None,
            "ltp": None,
            "current_value": None,
            "pnl_absolute": None,
            "pnl_pct": None,
            "milestone_contribution_daily": None,
        })
    return result


def get_holding_detail(db: Session, holding_id: int):
    return db.query(models.Holding).filter(models.Holding.id == holding_id).first()


def create_holding(db: Session, payload: HoldingCreate):
    holding = models.Holding(**payload.dict())
    db.add(holding)
    db.commit()
    db.refresh(holding)
    return holding


def get_summary(db: Session):
    holdings = db.query(models.Holding).filter(models.Holding.is_active == True).all()
    return {
        "total_holdings": len(holdings),
        "total_value": None,
        "total_pnl": None,
        "health": "PENDING_FIRST_SYNC",
        "message": "Run Layer 1 sync to see live data"
    }


def get_allocation_breakdown(db: Session):
    holdings = db.query(models.Holding).filter(models.Holding.is_active == True).all()
    return [{"tradingsymbol": h.tradingsymbol, "category": h.category, "allocation_pct": None}
            for h in holdings]
