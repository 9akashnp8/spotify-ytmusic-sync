import logging
from typing import List
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Cookie
from typing import Optional
from queue import Queue
from fastapi.websockets import WebSocket

from models import SpotifyPlaylistCollection, YTMusicSearchPayload
from services import (
    SpotifyService,
    yt_music_search_wrapper,
    get_or_create_collection,
    get_docs_from_collection,
    yt_music_like_wrapper,
)
from utils import MOCK_SPOTIFY_PLAYLIST_SONGS, MOCK_YTMUSIC_SEARCH_RESULT

logger = logging.getLogger(__name__)
spotify_service = SpotifyService()
queue = Queue()

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


@app.post("/youtube-music/sync")
async def search_youtube_music(
    payload: List[YTMusicSearchPayload],
    backgroud_task: BackgroundTasks 
) -> Response:
    """
    Core sync endpoint that takes list of spotify
    songs and likes the same in users YTMusic account.

    The sync is run in the background, with live status
    pushed as SSE.
    """
    backgroud_task.add_task(sync_ytmusic_spotify, payload)

    return JSONResponse(content={
        "status": "success",
        "message": "Task queued, Please wait as we sync songs"
    })