import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")


async def run_layer1_sync():
    """
    Layer 1 — Data sync and computation.
    Runs at 3:45 PM IST every weekday (15 min after market close).
    Fetches all Kite API data and computes 4 scores per holding.
    """
    logger.info("=== Layer 1 sync starting ===")
    try:
        # Import here to avoid circular imports at startup
        from backend.layer1.runner import run_layer1
        await run_layer1()
        logger.info("=== Layer 1 sync complete ===")
    except Exception as e:
        logger.error(f"Layer 1 sync failed: {e}", exc_info=True)


async def run_layer2_decisions():
    """
    Layer 2 — Decision engine.
    Runs at 4:15 PM IST every weekday (30 min after market close).
    Reads Layer 1 scores, applies Cat A/B/C rules, fires recommendations.
    """
    logger.info("=== Layer 2 decisions starting ===")
    try:
        from backend.layer2.runner import run_layer2
        await run_layer2()
        logger.info("=== Layer 2 decisions complete ===")
    except Exception as e:
        logger.error(f"Layer 2 decisions failed: {e}", exc_info=True)


async def compute_recommendation_outcomes():
    """
    5-day outcome computation.
    Runs at 9:00 AM IST every weekday.
    Calculates outcome for recommendations fired exactly 5 trading days ago.
    """
    logger.info("=== Outcome computation starting ===")
    try:
        from backend.layer2.outcomes import compute_outcomes
        await compute_outcomes()
        logger.info("=== Outcome computation complete ===")
    except Exception as e:
        logger.error(f"Outcome computation failed: {e}", exc_info=True)


# Register all jobs
scheduler.add_job(
    run_layer1_sync,
    CronTrigger(day_of_week="mon-fri", hour=15, minute=45),
    id="layer1_sync",
    replace_existing=True,
    misfire_grace_time=300,  # Allow 5 min grace if server was briefly down
)

scheduler.add_job(
    run_layer2_decisions,
    CronTrigger(day_of_week="mon-fri", hour=16, minute=15),
    id="layer2_decisions",
    replace_existing=True,
    misfire_grace_time=300,
)

scheduler.add_job(
    compute_recommendation_outcomes,
    CronTrigger(day_of_week="mon-fri", hour=9, minute=0),
    id="outcome_computation",
    replace_existing=True,
    misfire_grace_time=300,
)
