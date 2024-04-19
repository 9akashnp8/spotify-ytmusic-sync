import requests
import logging
from typing import List
from ytmusicapi import YTMusic
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Cookie
from typing import Optional

from models import Song
from services import SpotifyService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
ytmusic = YTMusic("oauth.json")
spotify_service = SpotifyService()

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

def like_songs(songs: List[Song]) -> None:
    for song in songs:
        song_from_yt = ytmusic.search(song.name)
        if song_from_yt[0]["category"] == "song":
            song_id, song_name = song_from_yt[0]["videoId"], song_from_yt[0]["title"]
            print(song_id, song_id)
        # ytmusic.rate_song(song_id, "LIKE")

@app.post("/auth/access-token")
def generate_access_token(response: Response):
    access_token = spotify_service.generate_access_token()
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
    songs = spotify_service.get_playlist_songs(playlist_id, access_token)
    return songs

@app.post("/youtube-music/search")
def search_youtube_music(payload: List[Song]):
    result = []
    for song in payload:
        yt_result = ytmusic.search(f"{song.name} - {song.artist}", "songs")
        name = yt_result[0]["title"]
        artists = ",".join([artist["name"] for artist in yt_result[0]["artists"]])
        if (song.name in name or name in song.name) and (song.artist in artists or artists in song.artist):
            match = 1
        else:
            match = 0
        song_id = yt_result[0]["videoId"]
        result.append(Song(song_id=song_id, platform="ytmusic", name=name, artist=artists))
    return result
