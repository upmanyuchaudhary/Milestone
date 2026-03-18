from sqlalchemy.orm import Session
import models


def get_active(db: Session):
    return (db.query(models.Recommendation)
              .filter(models.Recommendation.user_action == None)
              .order_by(models.Recommendation.milestone_impact_days.desc())
              .all())


def record_action(db: Session, alert_id: int, action: str):
    alert = db.query(models.Recommendation).filter(models.Recommendation.id == alert_id).first()
    if not alert:
        return None
    alert.user_action = action
    db.commit()
    return alert


def get_history(db: Session):
    return (db.query(models.Recommendation)
              .filter(models.Recommendation.user_action != None)
              .order_by(models.Recommendation.fired_at.desc())
              .limit(10)
              .all())


def get_ignored(db: Session):
    return (db.query(models.Recommendation)
              .filter(models.Recommendation.user_action == "IGNORED")
              .all())


def get_accuracy_log(db: Session):
    return db.query(models.SignalAccuracyLog).all() if hasattr(models, 'SignalAccuracyLog') else []