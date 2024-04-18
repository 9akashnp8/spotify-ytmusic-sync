import logging
import requests
from typing import List, Dict, Any
from decouple import config

from models import Song

logger = logging.getLogger(__name__)

class SpotifyService():
    CLIENT_ID = config("CLIENT_ID")
    CLIENT_SECRET = config("CLIENT_SECRET")
    API_BASE_URL = "https://api.spotify.com/v1"

    def generate_access_token(self) -> str:
        headers = { "Content-Type": "application/x-www-form-urlencoded" }
        body = f"grant_type=client_credentials&client_id={self.CLIENT_ID}&client_secret={self.CLIENT_SECRET}"
        url = "https://accounts.spotify.com/api/token"
        response = requests.post(url, data=body, headers=headers )
        if response.ok:
            data = response.json()
            access_token = data.get("access_token", "")
            return access_token

    def _extract_song_details(self, songs: List[Dict[str, Any]]) -> List[Song]:
        result = []
        for song in songs:
            song_id = song["track"]["id"]
            title = song["track"]["name"]
            artist = song["track"]["artists"][0]["name"]
            result.append(
                Song(song_id=song_id, platform="spotify", name=title, artist=artist)
            )
        return result
            
    def get_playlist_songs(self, playlist_id: str, access_token: str) -> List[Song]:
        headers = { "Authorization": f"Bearer {access_token}" }
        response = requests.get(
            f"{self.API_BASE_URL}/playlists/{playlist_id}",
            headers=headers
        )
        if response.ok:
            data = response.json()
            tracks = data["tracks"]["items"]
            songs = self._extract_song_details(tracks)
            return songs
        else:
            logger.error(f"""
                Something went wrong when fetching soptify playlist songs: {response.text}
            """)
