import requests
import logging
from typing import List
from decouple import config
from ytmusicapi import YTMusic
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Cookie
from typing import Optional

from models import UserLikedTracks

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
ytmusic = YTMusic("oauth.json")
CLIENT_ID = config("CLIENT_ID")
CLIENT_SECRET = config("CLIENT_SECRET")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["GET", "POST", "HEAD", "OPTIONS"],
    allow_headers=[
        "Access-Control-Allow-Headers",
        "Content-Type",
        "Authorization",
        "Access-Control-Allow-Origin",
        "Set-Cookie"
    ],
)

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

def get_playlist_songs(playlist_id: str, access_token: str) -> List[UserLikedTracks]:
    headers = { "Authorization": f"Bearer {access_token}" }
    response = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}", headers=headers)
    if response.ok:
        data = response.json()
        tracks = data["tracks"]["items"]
        tracks = [UserLikedTracks(name=item["track"]["name"], artist=item["track"]["artists"][0]["name"]) for item in tracks]
        return tracks
    else:
        logger.error(f"""
            Something went wrong when fetching soptify playlist songs: {response.text}
        """)


def like_songs(songs: List[UserLikedTracks]) -> None:
    for song in songs:
        song_from_yt = ytmusic.search(song.name)
        if song_from_yt[0]["category"] == "song":
            song_id, song_name = song_from_yt[0]["videoId"], song_from_yt[0]["title"]
            print(song_id, song_id)
        # ytmusic.rate_song(song_id, "LIKE")

@app.post("/auth/access-token")
def generate_access_token(response: Response):
    access_token = get_access_token()
    response.set_cookie(
        "access_token",
        value=access_token,
        httponly=True,
        samesite="none",
        max_age=1800,
        expires=1800,
    )
    return {"status": "success"}


@app.get("/spotify/playlists/{playlist_id}/songs")
def get_spotify_playlist_songs(playlist_id: str, access_token: Optional[str] = Cookie(None)):
    songs = get_playlist_songs(playlist_id, access_token)
    return songs

@app.post("/youtube-music/search")
def search_youtube_music(payload: List[UserLikedTracks]):
    result = []
    for song in payload:
        yt_result = ytmusic.search(f"{song.name} - {song.artist}", "songs")
        title = yt_result[0]["title"]
        artists = ",".join([artist["name"] for artist in yt_result[0]["artists"]])
        if (song.name in title or title in song.name) and (song.artist in artists or artists in song.artist):
            match = 1
        else:
            match = 0
        data = {
            "videoId": yt_result[0]["videoId"],
            "category": yt_result[0]["category"],
            "title": title,
            "artist": artists,
            "match": match
        }
        result.append(data)
    return result
