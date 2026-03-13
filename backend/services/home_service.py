"""
Home dashboard service — Sprint 0 placeholder.
Assembles all data for Screen 1 in a single call.
"""
from sqlalchemy.orm import Session
from backend import models
from backend.services.milestone_service import get_progress


def build_dashboard(db: Session):
    progress = get_progress(db)
    active_alerts = (db.query(models.Recommendation)
                       .filter(models.Recommendation.user_action == None)
                       .count())
    holdings = db.query(models.Holding).filter(models.Holding.is_active == True).all()
    story_cards = []
    if not holdings:
        story_cards.append({
            "type": "WATCH",
            "text": "Add your holdings to get started",
            "subtext": "Use POST /portfolio/holdings to add your portfolio"
        })
    elif active_alerts > 0:
        story_cards.append({
            "type": "ALERT",
            "text": f"{active_alerts} recommendation{'s' if active_alerts > 1 else ''} waiting for your review",
            "subtext": "Check the Alerts screen"
        })
    else:
        story_cards.append({
            "type": "POSITIVE",
            "text": "Your portfolio needs no attention today",
            "subtext": "All holdings within thresholds"
        })

    return {
        "milestone_progress": progress,
        "portfolio_health": "PENDING_FIRST_SYNC" if not holdings else "HEALTHY",
        "total_value": progress.get("current_value", 0),
        "day_change": 0,
        "day_change_pct": 0,
        "active_alert_count": active_alerts,
        "story_cards": story_cards,
    }
