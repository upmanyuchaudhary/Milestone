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


def sync_holdings_to_db(db: Session, holdings: list):
    db.query(models.Holding).update({"is_active": False})
    db.commit()

    synced = 0
    for h in holdings:
        existing = db.query(models.Holding).filter(
            models.Holding.tradingsymbol == h["tradingsymbol"],
            models.Holding.exchange == h["exchange"]
        ).first()

        if existing:
            existing.quantity = h["quantity"]
            existing.average_buy_price = h["average_buy_price"]
            existing.is_active = True
        else:
            new_holding = models.Holding(
                tradingsymbol=h["tradingsymbol"],
                exchange=h["exchange"],
                quantity=h["quantity"],
                average_buy_price=h["average_buy_price"],
                category=h.get("category", "EQUITY"),
                is_active=True,
            )
            db.add(new_holding)
        synced += 1

    db.commit()
    return {"status": "success", "synced": synced}