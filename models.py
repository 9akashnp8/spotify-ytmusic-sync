from pydantic import BaseModel, BeforeValidator, Field
from typing import Annotated, Optional, List

PyObjectId = Annotated[str, BeforeValidator(str)]

class SpotifySong(BaseModel):
    """
    Spotify Song model
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    song_id: str = Field(...)
    name: str = Field(...)
    artist: str = Field(...)
    found: bool = Field(...)
    liked: bool = Field(...)


class SpotifyPlaylistCollection(BaseModel):
    songs: List[SpotifySong]


class YTMusicSearchPayload(BaseModel):
    song_id: str
    name: str
    artist: str


class YTMusicSearchResult(BaseModel):
    source_song_id: str
    ytmusic_song_id: str
    name: str
    artist: str

