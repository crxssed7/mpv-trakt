import requests

from config import TRAKT_CLIENT_ID

class TraktClient:
    def __init__(self):
        self.base_url = "https://api.trakt.tv"
        self.headers = {
            "Content-Type": "application/json",
            "trakt-api-version": "2",
            "trakt-api-key": TRAKT_CLIENT_ID
        }

    def search(self, query):
        print(f"Searching Trakt for: {query}")
        data = self._send_request({"query": query}, "search/movie,show")
        return data

    def _send_request(self, body, endpoint):
        res = requests.get(f"{self.base_url}/{endpoint}", params=body, headers=self.headers)
        if res.status_code == 200:
            return res.json()
        return None
