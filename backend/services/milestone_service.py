"""
Milestone service — Sprint 0 placeholder.
Real implementation built in Sprint 2.
"""
from sqlalchemy.orm import Session
from backend import models
from backend.schemas import ScenarioRequest, MilestoneConfigUpdate
from datetime import date, timedelta
from decimal import Decimal


def get_progress(db: Session):
    config = db.query(models.UserConfig).first()
    if not config:
        return {
            "current_value": 0, "target_value": 0, "progress_pct": 0,
            "projected_date": date.today(), "days_ahead_behind": 0,
            "required_monthly": 0, "this_month_growth": 0,
            "start_value": 0, "start_date": date.today()
        }
    return {
        "current_value": float(config.portfolio_start_value),
        "target_value": float(config.milestone_target),
        "progress_pct": round(float(config.portfolio_start_value) / float(config.milestone_target) * 100, 2),
        "projected_date": config.milestone_date,
        "days_ahead_behind": 0,
        "required_monthly": float(config.monthly_sip_amount),
        "this_month_growth": 0,
        "start_value": float(config.portfolio_start_value),
        "start_date": config.portfolio_start_date,
    }


def get_history(db: Session):
    return db.query(models.MilestoneHistory).order_by(models.MilestoneHistory.month_year).all()


def get_contribution_breakdown(db: Session):
    return {"equity_appreciation_pct": 0, "sip_pct": 0, "rebalancing_pct": 0,
            "message": "Data builds after first month of tracking"}


def compute_scenario(db: Session, payload: ScenarioRequest):
    config = db.query(models.UserConfig).first()
    if not config:
        return {"projected_date": date.today(), "months_to_target": 0, "days_delta": 0, "required_monthly": 0}

    target = float(payload.target_amount or config.milestone_target)
    current = float(config.portfolio_start_value)
    monthly = float(payload.monthly_sip or config.monthly_sip_amount)
    months_needed = max(1, int((target - current) / monthly)) if monthly > 0 else 999
    projected = date.today() + timedelta(days=months_needed * 30)
    return {
        "projected_date": projected,
        "months_to_target": months_needed,
        "days_delta": 0,
        "required_monthly": monthly,
    }


def update_milestone_config(db: Session, payload: MilestoneConfigUpdate):
    config = db.query(models.UserConfig).first()
    if not config:
        return {"error": "No config found"}
    for field, value in payload.dict(exclude_none=True).items():
        setattr(config, field, value)
    db.commit()
    return {"status": "updated"}
