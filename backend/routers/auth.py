import os
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db

router = APIRouter()


@router.get("/login-url")
def get_login_url():
    """Returns the Kite login URL for the user to authenticate."""
    from kiteconnect import KiteConnect
    kite = KiteConnect(api_key=os.getenv("KITE_API_KEY"))
    return {"login_url": kite.login_url()}


@router.post("/callback")
def auth_callback(request_token: str, db: Session = Depends(get_db)):
    """
    Exchanges the request_token (from Kite callback URL) for an access_token.
    Stores the access_token in the environment for scheduled jobs to use.
    """
    from kiteconnect import KiteConnect
    kite = KiteConnect(api_key=os.getenv("KITE_API_KEY"))
    session = kite.generate_session(
        request_token,
        api_secret=os.getenv("KITE_API_SECRET")
    )
    access_token = session["access_token"]

    # Store in memory for this process — persists until Railway restarts
    os.environ["KITE_ACCESS_TOKEN"] = access_token
    return {"status": "authenticated", "message": "Token set. Jobs will use this token today."}


@router.get("/status")
def get_auth_status():
    """Check if a valid access token is currently stored."""
    token = os.getenv("KITE_ACCESS_TOKEN", "")
    return {
        "valid": bool(token),
        "message": "Token present" if token else "No token — please login via /auth/login-url"
    }
