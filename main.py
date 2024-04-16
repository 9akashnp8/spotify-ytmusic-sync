import requests
from typing import List
from decouple import config

from models import UserLikedTracks

CLIENT_ID = config("CLIENT_ID")
CLIENT_SECRET = config("CLIENT_SECRET")

def get_access_token() -> str:
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    body = f"grant_type=client_credentials&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}"
    url = "https://accounts.spotify.com/api/token"
    response = requests.post(url, data=body, headers=headers )
    if response.ok:
        data = response.json()
        access_token = data.get("access_token", "")
        return access_token

def get_user_liked_tracks(playlist_id: str) -> List[UserLikedTracks]:
    headers = { "Authorization": f"Bearer {config('ACCESS_TOKEN')}" }
    response = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}", headers=headers)
    if response.ok:
        data = response.json()
        tracks = data["tracks"]["items"]
        tracks = [{"name": item["track"]["name"], "artist": item["track"]["artists"][0]["name"]} for item in tracks]
        return tracks

print(get_user_liked_tracks("37i9dQZEVXcO9m01hH7fa7"))