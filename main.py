import concurrent.futures
import logging
from typing import List
from ytmusicapi import YTMusic
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Cookie
from typing import Optional

from models import YTMusicSearchResult, SpotifySong, SpotifyPlaylistCollection
from services import (
    SpotifyService,
    yt_music_search_wrapper,
    get_or_create_collection,
    get_docs_from_collection,
)
from utils import MOCK_SPOTIFY_PLAYLIST_SONGS, MOCK_YTMUSIC_SEARCH_RESULT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
ytmusic = YTMusic("oauth.json")
spotify_service = SpotifyService()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "HEAD", "OPTIONS"],
    allow_headers=[
        "Access-Control-Allow-Headers",
        "Content-Type",
        "Authorization",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Credentials",
        "Set-Cookie"
    ],
)

def like_songs(songs: List[SpotifySong]) -> None:
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
        samesite="lax",
        max_age=1800,
        expires=1800,
    )
    return {"status": "success"}


@app.get("/spotify/playlists/{playlist_id}/songs")
async def get_spotify_playlist_songs(
    playlist_id: str,
    mock: Optional[bool] = False,
    access_token: Optional[str] = Cookie(None)
):
    if mock:
        return MOCK_SPOTIFY_PLAYLIST_SONGS
    is_created, collection = await get_or_create_collection(playlist_id)
    if is_created:
        playlist_songs = spotify_service.get_playlist_songs(playlist_id, access_token)
        collection.insert_many(playlist_songs)
        return SpotifyPlaylistCollection(songs=playlist_songs)
    documents = await get_docs_from_collection(collection)
    return SpotifyPlaylistCollection(songs=documents)


@app.post("/youtube-music/search")
async def search_youtube_music(payload: List[SpotifySong], mock: Optional[bool] = False) -> List[YTMusicSearchResult]:
    if mock:
        return MOCK_YTMUSIC_SEARCH_RESULT
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_results = [executor.submit(yt_music_search_wrapper, song.song_id, song.name, song.artist) for song in payload]
        results = [future.result() for future in future_results]
        return results
