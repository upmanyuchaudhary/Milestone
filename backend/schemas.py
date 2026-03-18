from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal


class HoldingCreate(BaseModel):
    tradingsymbol: str
    exchange: str
    isin: str
    category: str
    quantity: int
    average_buy_price: Decimal
    stop_loss_price: Optional[Decimal] = None
    entry_date: date
    intended_holding_period: Optional[int] = None


class HoldingScores(BaseModel):
    trend_strength_score:   Optional[Decimal] = None
    orderbook_score:        Optional[Decimal] = None
    portfolio_health_score: Optional[Decimal] = None
    milestone_score:        Optional[Decimal] = None
    composite_score:        Optional[Decimal] = None
    output_state:           Optional[str] = None
    score_date:             Optional[date] = None


class HoldingResponse(BaseModel):
    id:                     int
    tradingsymbol:          str
    exchange:               str
    category:               str
    quantity:               int
    average_buy_price:      Decimal
    stop_loss_price:        Optional[Decimal]
    entry_date:             date
    is_active:              bool
    latest_scores:          Optional[HoldingScores] = None
    ltp:                    Optional[Decimal] = None
    current_value:          Optional[Decimal] = None
    pnl_absolute:           Optional[Decimal] = None
    pnl_pct:                Optional[Decimal] = None

    class Config:
        from_attributes = True


class MilestoneProgress(BaseModel):
    current_value:        Decimal
    target_value:         Decimal
    progress_pct:         Decimal
    projected_date:       date
    days_ahead_behind:    int
    required_monthly:     Decimal
    this_month_growth:    Decimal
    start_value:          Decimal
    start_date:           date


class MilestoneHistoryItem(BaseModel):
    month_year:          str
    portfolio_value:     Decimal
    monthly_change:      Decimal
    sip_deployed:        Decimal
    milestone_pct:       Decimal
    days_ahead_behind:   int
    projected_completion: date


class ScenarioRequest(BaseModel):
    monthly_sip:     Optional[Decimal] = None
    target_amount:   Optional[Decimal] = None
    target_date:     Optional[date] = None


class ScenarioResponse(BaseModel):
    projected_date:       date
    months_to_target:     int
    days_delta:           int
    required_monthly:     Decimal


class MilestoneConfigUpdate(BaseModel):
    milestone_target:    Optional[Decimal] = None
    milestone_date:      Optional[date] = None
    monthly_sip_amount:  Optional[Decimal] = None
    sip_date:            Optional[int] = None
    concentration_limit: Optional[Decimal] = None


class AlertResponse(BaseModel):
    id:                   int
    tradingsymbol:        str
    category:             str
    recommendation_type:  str
    output_state:         str
    composite_score:      Decimal
    signals_agreeing:     int
    persistence_days:     int
    rupee_impact:         Decimal
    milestone_impact_days: int
    plain_language_text:  str
    ltp_at_fire:          Decimal
    fired_at:             datetime
    user_action:          Optional[str]

    class Config:
        from_attributes = True


class AlertActionRequest(BaseModel):
    action: str


class AccuracyResponse(BaseModel):
    month_year:            str
    total_recommendations: int
    accuracy_pct:          Decimal
    total_value_generated: Decimal
    cost_of_ignoring:      Decimal


class StoryCard(BaseModel):
    type:    str
    text:    str
    subtext: Optional[str] = None


class HomeDashboard(BaseModel):
    milestone_progress:   MilestoneProgress
    portfolio_health:     str
    total_value:          Decimal
    day_change:           Decimal
    day_change_pct:       Decimal
    active_alert_count:   int
    story_cards:          List[StoryCard]