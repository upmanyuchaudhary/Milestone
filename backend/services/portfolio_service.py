from sqlalchemy.orm import Session
import models


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
            "average_buy_price": h.average_buy_price,
            "stop_loss_price": h.stop_loss_price,
            "entry_date": h.entry_date,
            "is_active": h.is_active,
        })
    return result


def get_holding_detail(db: Session, holding_id: int):
    return db.query(models.Holding).filter(models.Holding.id == holding_id).first()


def create_holding(db: Session, payload):
    holding = models.Holding(**payload)
    db.add(holding)
    db.commit()
    db.refresh(holding)
    return holding


def get_summary(db: Session):
    holdings = db.query(models.Holding).filter(models.Holding.is_active == True).all()
    total_value = sum(h.quantity * h.average_buy_price for h in holdings)
    return {
        "total_value": total_value,
        "total_holdings": len(holdings),
        "portfolio_health": "HEALTHY"
    }


def get_allocation_breakdown(db: Session):
    holdings = db.query(models.Holding).filter(models.Holding.is_active == True).all()
    total = sum(h.quantity * h.average_buy_price for h in holdings)
    result = []
    for h in holdings:
        value = h.quantity * h.average_buy_price
        pct = (value / total * 100) if total else 0
        result.append({
            "tradingsymbol": h.tradingsymbol,
            "value": value,
            "pct": pct
        })
    return result