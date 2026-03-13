import os
from fastapi import APIRouter

router = APIRouter()


@router.get("/login-url")
def get_login_url():
    from kiteconnect import KiteConnect
    kite = KiteConnect(api_key=os.getenv("KITE_API_KEY"))
    return {"login_url": kite.login_url()}


@router.get("/status")
def get_auth_status():
    token = os.getenv("KITE_ACCESS_TOKEN", "")
    return {
        "valid": bool(token),
        "message": "Token present" if token else "No token — please login via /auth/login-url"
    }


@router.post("/callback")
def auth_callback(request_token: str):
    from kiteconnect import KiteConnect
    kite = KiteConnect(api_key=os.getenv("KITE_API_KEY"))
    session = kite.generate_session(
        request_token,
        api_secret=os.getenv("KITE_API_SECRET")
    )
    os.environ["KITE_ACCESS_TOKEN"] = session["access_token"]
    return {"status": "authenticated", "message": "Token set successfully."}