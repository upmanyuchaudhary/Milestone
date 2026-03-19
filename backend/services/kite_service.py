import os
from kiteconnect import KiteConnect


def get_kite():
    kite = KiteConnect(api_key=os.getenv("KITE_API_KEY"))
    kite.set_access_token(os.getenv("KITE_ACCESS_TOKEN"))
    return kite


def fetch_holdings():
    kite = get_kite()
    holdings = kite.holdings()
    result = []
    for h in holdings:
        result.append({
            "tradingsymbol": h["tradingsymbol"],
            "exchange": h["exchange"],
            "quantity": h["quantity"],
            "average_buy_price": h["average_price"],
            "category": "EQUITY",
            "is_active": True,
        })
    return result


def fetch_positions():
    kite = get_kite()
    positions = kite.positions()
    return positions.get("net", [])