from pydantic import BaseModel

class Song(BaseModel):
    song_id: str
    platform: str
    name: str
    artist: str
