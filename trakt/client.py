import time
import requests

from config import TRAKT_CLIENT_ID
from trakt.auth import get_stored_token, poll_token, refresh_token, request_device_code
from ui.session import SESSION

class TraktClient:
    def __init__(self):
        self.base_url = "https://api.trakt.tv"
        self.token = get_stored_token()

    def authenticate(self):
        if self.token:
            self._refresh_token_if_needed()
            return
        device_data = request_device_code()
        print(f"Please go to {device_data['verification_url']} and enter code: {device_data['user_code']}")
        self.token = poll_token(
            device_data["device_code"],
            device_data["interval"],
            device_data["expires_in"]
        )

    def search(self, query):
        print(f"Searching Trakt for: {query}")
        data = self._send_request("search/movie,show", params={"query": query})
        return data

    def start_scrobble(self, item):
        print(f"Starting scrobble for {item}")
        data = self._send_request("scrobble/start", body=item, method="POST")
        if data:
            SESSION.start(item)
        return data

    def pause_scrobble(self):
        if not SESSION.is_active():
            print("No active scrobble session")
            return
        item = SESSION.active_item
        print(f"Pausing scrobble for {item}")
        data = self._send_request("scrobble/pause", body=item, method="POST")
        if data:
            SESSION.pause()
        return data

    def resume_scrobble(self):
        if not SESSION.is_active():
            print("No active scrobble session")
            return
        item = SESSION.active_item
        print(f"Resuming scrobble for {item}")
        data = self._send_request("scrobble/start", body=item, method="POST")
        if data:
            SESSION.resume()
        return data

    def stop_scrobble(self):
        if not SESSION.is_active():
            print("No active scrobble session")
            return
        item = SESSION.active_item
        print(f"Stopping scrobble for {item}")
        data = self._send_request("scrobble/stop", body=item, method="POST")
        if data:
            SESSION.stop()
        return data

    def _send_request(self, endpoint, body=None, params=None, method="GET"):
        res = requests.request(method, f"{self.base_url}/{endpoint}", json=body, params=params, headers=self._headers())
        if res.status_code < 300:
            return res.json()
        else:
            print(f"Error: {res.status_code} - {res.text}")
        return None

    def _refresh_token_if_needed(self):
        if self.token and self.token.get("expires_at", 0) < time.time():
            self.token = refresh_token(self.token)

    def _headers(self):
        h = {
            "Content-Type": "application/json",
            "trakt-api-version": "2",
            "trakt-api-key": TRAKT_CLIENT_ID,
        }
        if self.token:
            h["Authorization"] = f"Bearer {self.token['access_token']}"
        return h
