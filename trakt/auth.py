import requests
import time
import json
from pathlib import Path

from config import TRAKT_CLIENT_ID, TRAKT_CLIENT_SECRET

TOKEN_PATH = Path("trakt_token.json")

def get_stored_token():
    if TOKEN_PATH.exists():
        with open(TOKEN_PATH, "r") as f:
            return json.load(f)
    return None

def save_token(token):
    expires_in = token.get("expires_in", 0)
    token["expires_at"] = time.time() + expires_in
    with open(TOKEN_PATH, "w") as f:
        json.dump(token, f)

def request_device_code():
    res = requests.post("https://api.trakt.tv/oauth/device/code", data={
        "client_id": TRAKT_CLIENT_ID
    })
    return res.json()

def poll_token(device_code, interval, expires_in):
    start = time.time()
    while time.time() - start < expires_in:
        res = requests.post("https://api.trakt.tv/oauth/device/token", data={
            "code": device_code,
            "client_id": TRAKT_CLIENT_ID,
            "client_secret": TRAKT_CLIENT_SECRET
        })

        if res.status_code == 200:
            token = res.json()
            save_token(token)
            return token
        elif res.status_code == 400:
            # still waiting
            time.sleep(interval)
        else:
            raise Exception(f"Token polling error: {res.text}")

    raise TimeoutError("User did not authenticate in time.")

def refresh_token(token):
    res = requests.post("https://api.trakt.tv/oauth/token", data={
        "grant_type": "refresh_token",
        "client_id": TRAKT_CLIENT_ID,
        "client_secret": TRAKT_CLIENT_SECRET,
        "refresh_token": token.get("refresh_token", ""),
        "grant_type": "refresh_token"
    })

    if res.status_code == 200:
        token = res.json()
        save_token(token)
        return token
    else:
        raise Exception(f"Token refresh error: {res.text}")
