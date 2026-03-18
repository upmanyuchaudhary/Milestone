from sqlalchemy import (
    Column, Integer, String, Numeric, Date, DateTime, Boolean,
    ForeignKey, Text, JSON, func
)
from sqlalchemy.orm import relationship
from database import Base


class UserConfig(Base):
    __tablename__ = "user_config"

    id                    = Column(Integer, primary_key=True, index=True)
    milestone_target      = Column(Numeric(12, 2), nullable=False)
    milestone_date        = Column(Date, nullable=False)
    portfolio_start_value = Column(Numeric(12, 2), nullable=False)
    portfolio_start_date  = Column(Date, nullable=False)
    monthly_sip_amount    = Column(Numeric(12, 2), nullable=False)
    sip_date              = Column(Integer, default=1)
    concentration_limit   = Column(Numeric(5, 2), default=25.00)


class Holding(Base):
    __tablename__ = "holdings"

    id                       = Column(Integer, primary_key=True, index=True)
    tradingsymbol            = Column(String(20), nullable=False)
    exchange                 = Column(String(10), nullable=False)
    isin                     = Column(String(12))
    category                 = Column(String(1), nullable=False)
    quantity                 = Column(Integer, nullable=False)
    average_buy_price        = Column(Numeric(12, 2), nullable=False)
    stop_loss_price          = Column(Numeric(12, 2))
    entry_date               = Column(Date, nullable=False)
    intended_holding_period  = Column(Integer)
    is_active                = Column(Boolean, default=True)
    scores                   = relationship("DailyScore", back_populates="holding")


class DailyScore(Base):
    __tablename__ = "daily_scores"

    id                    = Column(Integer, primary_key=True, index=True)
    holding_id            = Column(Integer, ForeignKey("holdings.id"), nullable=False)
    score_date            = Column(Date, nullable=False)
    trend_strength_score  = Column(Numeric(5, 2))
    orderbook_score       = Column(Numeric(5, 2))
    portfolio_health_score= Column(Numeric(5, 2))
    milestone_score       = Column(Numeric(5, 2))
    composite_score       = Column(Numeric(5, 2))
    output_state          = Column(String(20))
    holding               = relationship("Holding", back_populates="scores")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id                    = Column(Integer, primary_key=True, index=True)
    holding_id            = Column(Integer, ForeignKey("holdings.id"), nullable=False)
    recommendation_type   = Column(String(20), nullable=False)
    output_state          = Column(String(20), nullable=False)
    composite_score       = Column(Numeric(5, 2))
    signals_agreeing      = Column(Integer)
    persistence_days      = Column(Integer)
    rupee_impact          = Column(Numeric(12, 2))
    milestone_impact_days = Column(Integer)
    plain_language_text   = Column(Text)
    ltp_at_fire           = Column(Numeric(12, 2))
    fired_at              = Column(DateTime, server_default=func.now())
    user_action           = Column(String(20))
    resolved_at           = Column(DateTime)


class MilestoneHistory(Base):
    __tablename__ = "milestone_history"

    id                   = Column(Integer, primary_key=True, index=True)
    month_year           = Column(String(7), nullable=False)
    portfolio_value      = Column(Numeric(12, 2))
    monthly_change       = Column(Numeric(12, 2))
    sip_deployed         = Column(Numeric(12, 2))
    milestone_pct        = Column(Numeric(5, 2))
    days_ahead_behind    = Column(Integer)
    projected_completion = Column(Date)