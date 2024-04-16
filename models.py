from pydantic import BaseModel

class UserLikedTracks(BaseModel):
    name: str
    artist: str
