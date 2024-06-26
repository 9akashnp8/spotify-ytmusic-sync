import json
from typing import List
from fastapi import FastAPI
from fastapi import Cookie
from typing import Optional
from sse_starlette import EventSourceResponse, ServerSentEvent
from fastapi.background import BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse

from models import SpotifyPlaylistCollection, YTMusicSearchPayload
from services import (
    SpotifyService,
    get_or_create_collection,
    get_docs_from_collection,
)
from utils import (
    MOCK_SPOTIFY_PLAYLIST_SONGS,
    sync_ytmusic_spotify,
    r_queue,
)

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

    # Store songs id to track. Gives us info on how many
    # times to lpop main status list.
    for song in payload:
        r_queue.lpush("song_tracker", song.song_id)
        

    # Delegate actual search and like task to background
    backgroud_task.add_task(sync_ytmusic_spotify, payload)

    return JSONResponse(content={
        "status": "success",
        "message": "Task queued, Please wait as we sync songs"
    })

async def get_song_status():
    """
    Generator that takes song status from
    redis queue and returns the same once found.

    `song_tracker` keeps track of how many songs
    were part of the request. Based on how many
    songs were requested, we wait for and extract
    the song status from `song_status`
    """
    for _ in range(r_queue.llen("song_tracker")):
        r_queue.lpop("song_tracker")
        __, song_data = r_queue.blpop("song_status")
        song = json.loads(song_data)
        yield ServerSentEvent(data=song)


@app.get("/sync-status")
def get_sync_status():
    """
    SSE Endpoint to send live updates on the `like`
    status of song(s) that were requested to be synced.
    """
    return EventSourceResponse(content=get_song_status())
