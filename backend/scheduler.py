import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")


async def run_layer1_sync():
    logger.info("=== Layer 1 sync starting ===")
    try:
        from layer1.runner import run_layer1
        await run_layer1()
    except Exception as e:
        logger.error(f"Layer 1 sync failed: {e}")


async def run_layer2_sync():
    logger.info("=== Layer 2 sync starting ===")
    try:
        from layer2.runner import run_layer2
        await run_layer2()
    except Exception as e:
        logger.error(f"Layer 2 sync failed: {e}")


scheduler.add_job(run_layer1_sync, CronTrigger(day_of_week="mon-fri", hour=15, minute=45))
scheduler.add_job(run_layer2_sync, CronTrigger(day_of_week="mon-fri", hour=16, minute=15))