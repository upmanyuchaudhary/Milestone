from sqlalchemy import (
    Column, Integer, String, Decimal, Date, DateTime, Boolean,
    ForeignKey, Text, JSON, func
)
from sqlalchemy.orm import relationship
from backend.database import Base


class UserConfig(Base):
    __tablename__ = "user_config"

    id                    = Column(Integer, primary_key=True, index=True)
    milestone_target      = Column(Decimal(12, 2), nullable=False)
    milestone_date        = Column(Date, nullable=False)
    portfolio_start_value = Column(Decimal(12, 2), nullable=False)
    portfolio_start_date  = Column(Date, nullable=False)
    monthly_sip_amount    = Column(Decimal(10, 2), nullable=False)
    sip_date              = Column(Integer, nullable=False)  # Day of month e.g. 17
    concentration_limit   = Column(Decimal(5, 2), default=25.00)
    created_at            = Column(DateTime, server_default=func.now())
    updated_at            = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Holding(Base):
    __tablename__ = "holdings"

    id                      = Column(Integer, primary_key=True, index=True)
    tradingsymbol           = Column(String(50), nullable=False, unique=True)
    exchange                = Column(String(10), nullable=False)  # NSE or BSE
    isin                    = Column(String(20), nullable=False)
    category                = Column(String(1), nullable=False)   # A, B, or C — fixed at entry
    quantity                = Column(Integer, nullable=False)
    average_buy_price       = Column(Decimal(10, 2), nullable=False)
    stop_loss_price         = Column(Decimal(10, 2), nullable=True)
    entry_date              = Column(Date, nullable=False)
    intended_holding_period = Column(Integer, nullable=True)      # Months
    is_active               = Column(Boolean, default=True)
    created_at              = Column(DateTime, server_default=func.now())

    # Relationships
    daily_scores       = relationship("DailyScore",         back_populates="holding")
    recommendations    = relationship("Recommendation",     back_populates="holding")
    persistence        = relationship("PersistenceCounter", back_populates="holding", uselist=False)
    rebalancing_events = relationship("RebalancingEvent",   back_populates="holding")


class DailyScore(Base):
    __tablename__ = "daily_scores"

    id                    = Column(Integer, primary_key=True, index=True)
    holding_id            = Column(Integer, ForeignKey("holdings.id"), nullable=False)
    score_date            = Column(Date, nullable=False)
    trend_strength_score  = Column(Decimal(4, 2), nullable=False)
    orderbook_score       = Column(Decimal(4, 2), nullable=False)
    portfolio_health_score= Column(Decimal(4, 2), nullable=False)
    milestone_score       = Column(Decimal(4, 2), nullable=False)
    composite_score       = Column(Decimal(4, 2), nullable=False)
    output_state          = Column(String(20), nullable=False)    # STRONG_HOLD to EXIT
    ltp                   = Column(Decimal(10, 2), nullable=False)
    portfolio_value       = Column(Decimal(12, 2), nullable=False)
    raw_scores_json       = Column(JSON, nullable=False)          # All sub-scores for ML logging
    computed_at           = Column(DateTime, server_default=func.now())

    holding = relationship("Holding", back_populates="daily_scores")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id                    = Column(Integer, primary_key=True, index=True)
    holding_id            = Column(Integer, ForeignKey("holdings.id"), nullable=False)
    recommendation_type   = Column(String(20), nullable=False)    # EXIT/REVIEW/WATCH/REBALANCE/SIP
    output_state          = Column(String(20), nullable=False)
    composite_score       = Column(Decimal(4, 2), nullable=False)
    signals_agreeing      = Column(Integer, nullable=False)
    persistence_days      = Column(Integer, nullable=False)
    rupee_impact          = Column(Decimal(10, 2), nullable=False)
    milestone_impact_days = Column(Integer, nullable=False)
    plain_language_text   = Column(Text, nullable=False)
    ltp_at_fire           = Column(Decimal(10, 2), nullable=False)
    fired_at              = Column(DateTime, server_default=func.now())
    user_action           = Column(String(20), nullable=True)     # ACTED/IGNORED/WATCHING
    action_at             = Column(DateTime, nullable=True)
    outcome_ltp           = Column(Decimal(10, 2), nullable=True)
    outcome_rupee         = Column(Decimal(10, 2), nullable=True)
    outcome_computed_at   = Column(DateTime, nullable=True)

    holding = relationship("Holding", back_populates="recommendations")


class MilestoneHistory(Base):
    __tablename__ = "milestone_history"

    id                    = Column(Integer, primary_key=True, index=True)
    month_year            = Column(String(10), nullable=False, unique=True)  # e.g. 2026-03
    portfolio_value       = Column(Decimal(12, 2), nullable=False)
    monthly_change        = Column(Decimal(12, 2), nullable=False)
    sip_deployed          = Column(Decimal(10, 2), nullable=False)
    milestone_pct         = Column(Decimal(5, 2), nullable=False)
    days_ahead_behind     = Column(Integer, nullable=False)        # Positive = ahead
    projected_completion  = Column(Date, nullable=False)
    equity_appreciation   = Column(Decimal(12, 2), nullable=False)
    rebalancing_gains     = Column(Decimal(12, 2), nullable=False)
    recorded_at           = Column(DateTime, server_default=func.now())


class PersistenceCounter(Base):
    __tablename__ = "persistence_counters"

    id            = Column(Integer, primary_key=True, index=True)
    holding_id    = Column(Integer, ForeignKey("holdings.id"), nullable=False, unique=True)
    watch_days    = Column(Integer, default=0)
    review_days   = Column(Integer, default=0)
    exit_days     = Column(Integer, default=0)
    last_good_days= Column(Integer, default=0)
    last_updated  = Column(Date, nullable=False)

    holding = relationship("Holding", back_populates="persistence")


class RebalancingEvent(Base):
    __tablename__ = "rebalancing_events"

    id                    = Column(Integer, primary_key=True, index=True)
    trigger_type          = Column(String(30), nullable=False)     # CONCENTRATION/REDEPLOYMENT/SIP
    holding_id            = Column(Integer, ForeignKey("holdings.id"), nullable=True)
    description           = Column(Text, nullable=False)
    rupee_amount          = Column(Decimal(10, 2), nullable=False)
    milestone_impact_days = Column(Integer, nullable=False)
    user_action           = Column(String(20), nullable=True)      # ACTED/IGNORED
    fired_at              = Column(DateTime, server_default=func.now())

    holding = relationship("Holding", back_populates="rebalancing_events")


class SignalAccuracyLog(Base):
    __tablename__ = "signal_accuracy_log"

    id                    = Column(Integer, primary_key=True, index=True)
    month_year            = Column(String(10), nullable=False, unique=True)
    total_recommendations = Column(Integer, nullable=False)
    acted_count           = Column(Integer, nullable=False)
    ignored_count         = Column(Integer, nullable=False)
    correct_count         = Column(Integer, nullable=False)
    total_value_generated = Column(Decimal(12, 2), nullable=False)
    cost_of_ignoring      = Column(Decimal(12, 2), nullable=False)
    accuracy_pct          = Column(Decimal(5, 2), nullable=False)
    computed_at           = Column(DateTime, server_default=func.now())
