from sqlalchemy.orm import Session
import models
from services.milestone_service import get_progress


def build_dashboard(db: Session):
    progress = get_progress(db)
    active_alerts = (db.query(models.Recommendation)
                       .filter(models.Recommendation.user_action == None)
                       .count())
    holdings = db.query(models.Holding).filter(models.Holding.is_active == True).all()

    total_value = sum(
        (h.quantity * h.average_buy_price) for h in holdings
    )

    return {
        "milestone_progress": progress,
        "portfolio_health": "HEALTHY",
        "total_value": total_value,
        "day_change": 0,
        "day_change_pct": 0,
        "active_alert_count": active_alerts,
        "story_cards": []
    }