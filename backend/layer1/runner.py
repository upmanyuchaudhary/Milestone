"""
Layer 1 Runner — Sprint 1 implementation.
This file is called by the scheduler at 3:45 PM daily.
"""
import logging

logger = logging.getLogger(__name__)


async def run_layer1():
    """
    Full Layer 1 execution:
    1. Fetch all active holdings from DB
    2. For each holding: fetch Kite quote + order book + historical
    3. Compute 4 scores (trend, orderbook, health, milestone)
    4. Write to daily_scores table
    """
    logger.info("Layer 1 runner — Sprint 1 not yet implemented")
    # Implementation added in Sprint 1
    pass
