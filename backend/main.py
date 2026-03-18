from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Milestone API",
    description="Autonomous portfolio manager for retail investors",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def create_tables():
    try:
        from database import engine, Base
        import models
        if engine:
            Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Table creation failed: {e}")

from routers import portfolio, milestone, alerts, auth, home

app.include_router(auth.router,      prefix="/auth",      tags=["Authentication"])
app.include_router(home.router,      prefix="/home",      tags=["Home"])
app.include_router(portfolio.router, prefix="/portfolio", tags=["Portfolio"])
app.include_router(milestone.router, prefix="/milestone", tags=["Milestone"])
app.include_router(alerts.router,    prefix="/alerts",    tags=["Alerts"])


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "milestone-api"}
