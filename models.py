from pydantic import BaseModel


class SpotifySong(BaseModel):
    song_id: str
    name: str
    artist: str


class YTMusicSearchResult(BaseModel):
    source_song_id: str
    ytmusic_song_id: str
    name: str
    artist: str
