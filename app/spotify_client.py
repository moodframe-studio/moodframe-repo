import os
import random
from typing import List, Dict
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from app.mood_to_genres import MOOD_TO_GENRES

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

auth_manager = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
)
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_tracks_for_mood(mood: str, limit: int = 1) -> List[Dict]:
    genres = MOOD_TO_GENRES.get(mood.lower())
    if not genres:
        return []

    tracks = []
    for genre in genres:
        result = sp.search(q=f"genre:{genre}", type="track", limit=5)
        for item in result["tracks"]["items"]:
            track = {
                "title": item["name"],
                "artist": item["artists"][0]["name"],
                "album_image": item["album"]["images"][0]["url"],
                "spotify_url": item["external_urls"]["spotify"],
                "popularity": item.get("popularity", 50),
                "language": "english"  # Optional: language detection can be added later
            }
            tracks.append(track)

    random.shuffle(tracks)
    return tracks[:limit]

