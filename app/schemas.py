from pydantic import BaseModel
from typing import List, Optional

class SongCreate(BaseModel):
    title: str
    artist: str
    album_image: str
    spotify_url: str
    popularity: Optional[int] = 50
    language: Optional[str] = "english"
    moods: List[str]

class UserFeedbackCreate(BaseModel):
    user_id: str
    song_id: int
    liked: bool
