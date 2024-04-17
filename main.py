import requests
from typing import List
from decouple import config
from ytmusicapi import YTMusic

from models import UserLikedTracks

ytmusic = YTMusic("oauth.json")
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
        tracks = [UserLikedTracks(name=item["track"]["name"], artist=item["track"]["artists"][0]["name"]) for item in tracks]
        return tracks


def like_songs(songs: List[UserLikedTracks]) -> None:
    for song in songs:
        song_from_yt = ytmusic.search(song.name)
        if song_from_yt[0]["category"] == "song":
            song_id, song_name = song_from_yt[0]["videoId"], song_from_yt[0]["title"]
            print(song_id, song_id)
        # ytmusic.rate_song(song_id, "LIKE")

print(like_songs(get_user_liked_tracks("6ITWYIfjMptEQMhmUp5Wsk")))