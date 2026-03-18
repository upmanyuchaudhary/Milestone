from sqlalchemy.orm import Session
import models
from datetime import date, timedelta
from decimal import Decimal


def get_progress(db: Session):
    config = db.query(models.UserConfig).first()
    if not config:
        return {
            "current_value": 0,
            "target_value": 600000,
            "progress_pct": 0,
            "projected_date": date.today(),
            "days_ahead_behind": 0,
            "required_monthly": 0,
            "this_month_growth": 0,
            "start_value": 0,
            "start_date": date.today()
        }

    holdings = db.query(models.Holding).filter(models.Holding.is_active == True).all()
    current_value = sum(h.quantity * h.average_buy_price for h in holdings)

    target = config.milestone_target
    progress_pct = (current_value / target * 100) if target else 0

    return {
        "current_value": current_value,
        "target_value": target,
        "progress_pct": progress_pct,
        "projected_date": config.milestone_date,
        "days_ahead_behind": 0,
        "required_monthly": config.monthly_sip_amount,
        "this_month_growth": 0,
        "start_value": config.portfolio_start_value,
        "start_date": config.portfolio_start_date
    }


def get_history(db: Session):
    return db.query(models.MilestoneHistory).all()


def get_contribution_breakdown(db: Session):
    return {"equity": 0, "sip": 0, "rebalancing": 0}


def compute_scenario(db: Session, payload):
    return {
        "projected_date": date.today(),
        "months_to_target": 0,
        "days_delta": 0,
        "required_monthly": 0
    }


def update_milestone_config(db: Session, payload):
    config = db.query(models.UserConfig).first()
    if not config:
        return {"error": "No config found"}
    if payload.get("milestone_target"):
        config.milestone_target = payload["milestone_target"]
    if payload.get("monthly_sip_amount"):
        config.monthly_sip_amount = payload["monthly_sip_amount"]
    db.commit()
    return {"status": "updated"}