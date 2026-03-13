"""
Alerts service — Sprint 0 placeholder.
Real implementation built in Sprint 2.
"""
from sqlalchemy.orm import Session
from backend import models
from datetime import datetime


def get_active(db: Session):
    return (db.query(models.Recommendation)
              .filter(models.Recommendation.user_action == None)
              .order_by(models.Recommendation.milestone_impact_days.desc())
              .all())


def record_action(db: Session, alert_id: int, action: str):
    rec = db.query(models.Recommendation).filter(models.Recommendation.id == alert_id).first()
    if not rec:
        return None
    rec.user_action = action
    rec.action_at = datetime.utcnow()
    db.commit()
    return rec


def get_history(db: Session):
    return (db.query(models.Recommendation)
              .filter(models.Recommendation.user_action != None)
              .order_by(models.Recommendation.action_at.desc())
              .limit(10)
              .all())


def get_ignored(db: Session):
    return (db.query(models.Recommendation)
              .filter(models.Recommendation.user_action == "IGNORED")
              .order_by(models.Recommendation.fired_at.desc())
              .all())


def get_accuracy_log(db: Session):
    return db.query(models.SignalAccuracyLog).order_by(models.SignalAccuracyLog.month_year.desc()).all()
