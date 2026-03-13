from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.database import engine, Base
from backend.scheduler import scheduler
from backend.routers import portfolio, milestone, alerts, auth, home


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start scheduled jobs on app startup
    scheduler.start()
    yield
    # Shutdown scheduler cleanly
    scheduler.shutdown()


app = FastAPI(
    title="Milestone API",
    description="Autonomous portfolio manager for retail investors",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten to Vercel URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router,      prefix="/auth",      tags=["Authentication"])
app.include_router(home.router,      prefix="/home",      tags=["Home"])
app.include_router(portfolio.router, prefix="/portfolio", tags=["Portfolio"])
app.include_router(milestone.router, prefix="/milestone", tags=["Milestone"])
app.include_router(alerts.router,    prefix="/alerts",    tags=["Alerts"])


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "milestone-api"}
