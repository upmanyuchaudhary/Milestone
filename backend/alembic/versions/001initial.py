"""create all tables

Revision ID: 001initial
Revises:
Create Date: 2026-03-13
"""
from alembic import op
import sqlalchemy as sa

revision = '001initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user_config',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('milestone_target', sa.Numeric(12, 2), nullable=False),
        sa.Column('milestone_date', sa.Date(), nullable=False),
        sa.Column('portfolio_start_value', sa.Numeric(12, 2), nullable=False),
        sa.Column('portfolio_start_date', sa.Date(), nullable=False),
        sa.Column('monthly_sip_amount', sa.Numeric(10, 2), nullable=False),
        sa.Column('sip_date', sa.Integer(), nullable=False),
        sa.Column('concentration_limit', sa.Numeric(5, 2), server_default='25.00'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('holdings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tradingsymbol', sa.String(50), nullable=False),
        sa.Column('exchange', sa.String(10), nullable=False),
        sa.Column('isin', sa.String(20), nullable=False),
        sa.Column('category', sa.String(1), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('average_buy_price', sa.Numeric(10, 2), nullable=False),
        sa.Column('stop_loss_price', sa.Numeric(10, 2), nullable=True),
        sa.Column('entry_date', sa.Date(), nullable=False),
        sa.Column('intended_holding_period', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tradingsymbol')
    )
    op.create_index('ix_holdings_id', 'holdings', ['id'])

    op.create_table('daily_scores',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('holding_id', sa.Integer(), nullable=False),
        sa.Column('score_date', sa.Date(), nullable=False),
        sa.Column('trend_strength_score', sa.Numeric(4, 2), nullable=False),
        sa.Column('orderbook_score', sa.Numeric(4, 2), nullable=False),
        sa.Column('portfolio_health_score', sa.Numeric(4, 2), nullable=False),
        sa.Column('milestone_score', sa.Numeric(4, 2), nullable=False),
        sa.Column('composite_score', sa.Numeric(4, 2), nullable=False),
        sa.Column('output_state', sa.String(20), nullable=False),
        sa.Column('ltp', sa.Numeric(10, 2), nullable=False),
        sa.Column('portfolio_value', sa.Numeric(12, 2), nullable=False),
        sa.Column('raw_scores_json', sa.JSON(), nullable=False),
        sa.Column('computed_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['holding_id'], ['holdings.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('recommendations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('holding_id', sa.Integer(), nullable=False),
        sa.Column('recommendation_type', sa.String(20), nullable=False),
        sa.Column('output_state', sa.String(20), nullable=False),
        sa.Column('composite_score', sa.Numeric(4, 2), nullable=False),
        sa.Column('signals_agreeing', sa.Integer(), nullable=False),
        sa.Column('persistence_days', sa.Integer(), nullable=False),
        sa.Column('rupee_impact', sa.Numeric(10, 2), nullable=False),
        sa.Column('milestone_impact_days', sa.Integer(), nullable=False),
        sa.Column('plain_language_text', sa.Text(), nullable=False),
        sa.Column('ltp_at_fire', sa.Numeric(10, 2), nullable=False),
        sa.Column('fired_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('user_action', sa.String(20), nullable=True),
        sa.Column('action_at', sa.DateTime(), nullable=True),
        sa.Column('outcome_ltp', sa.Numeric(10, 2), nullable=True),
        sa.Column('outcome_rupee', sa.Numeric(10, 2), nullable=True),
        sa.Column('outcome_computed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['holding_id'], ['holdings.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('milestone_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('month_year', sa.String(10), nullable=False),
        sa.Column('portfolio_value', sa.Numeric(12, 2), nullable=False),
        sa.Column('monthly_change', sa.Numeric(12, 2), nullable=False),
        sa.Column('sip_deployed', sa.Numeric(10, 2), nullable=False),
        sa.Column('milestone_pct', sa.Numeric(5, 2), nullable=False),
        sa.Column('days_ahead_behind', sa.Integer(), nullable=False),
        sa.Column('projected_completion', sa.Date(), nullable=False),
        sa.Column('equity_appreciation', sa.Numeric(12, 2), nullable=False),
        sa.Column('rebalancing_gains', sa.Numeric(12, 2), nullable=False),
        sa.Column('recorded_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('month_year')
    )

    op.create_table('persistence_counters',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('holding_id', sa.Integer(), nullable=False),
        sa.Column('watch_days', sa.Integer(), server_default='0'),
        sa.Column('review_days', sa.Integer(), server_default='0'),
        sa.Column('exit_days', sa.Integer(), server_default='0'),
        sa.Column('last_good_days', sa.Integer(), server_default='0'),
        sa.Column('last_updated', sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(['holding_id'], ['holdings.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('holding_id')
    )

    op.create_table('rebalancing_events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('trigger_type', sa.String(30), nullable=False),
        sa.Column('holding_id', sa.Integer(), nullable=True),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('rupee_amount', sa.Numeric(10, 2), nullable=False),
        sa.Column('milestone_impact_days', sa.Integer(), nullable=False),
        sa.Column('user_action', sa.String(20), nullable=True),
        sa.Column('fired_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['holding_id'], ['holdings.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('signal_accuracy_log',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('month_year', sa.String(10), nullable=False),
        sa.Column('total_recommendations', sa.Integer(), nullable=False),
        sa.Column('acted_count', sa.Integer(), nullable=False),
        sa.Column('ignored_count', sa.Integer(), nullable=False),
        sa.Column('correct_count', sa.Integer(), nullable=False),
        sa.Column('total_value_generated', sa.Numeric(12, 2), nullable=False),
        sa.Column('cost_of_ignoring', sa.Numeric(12, 2), nullable=False),
        sa.Column('accuracy_pct', sa.Numeric(5, 2), nullable=False),
        sa.Column('computed_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('month_year')
    )


def downgrade():
    op.drop_table('signal_accuracy_log')
    op.drop_table('rebalancing_events')
    op.drop_table('persistence_counters')
    op.drop_table('milestone_history')
    op.drop_table('recommendations')
    op.drop_table('daily_scores')
    op.drop_index('ix_holdings_id', table_name='holdings')
    op.drop_table('holdings')
    op.drop_table('user_config')
