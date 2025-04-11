from fastapi import FastAPI, Query, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional

from app.spotify_client import get_tracks_for_mood
from app.routes import router as analyze_router
from app.model.models import Base, Song, UserFeedback, Mood
from app.model.database import engine, SessionLocal
from pydantic import BaseModel

# -------------------------------
# Create DB tables
Base.metadata.create_all(bind=engine)

# -------------------------------
# Initialize FastAPI app
app = FastAPI()

# -------------------------------
# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Register additional routes
app.include_router(analyze_router)

# -------------------------------
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------------
# Pydantic model for incoming song
class SongCreate(BaseModel):
    title: str
    artist: str
    album_image: str
    spotify_url: str
    popularity: Optional[int] = 50
    language: Optional[str] = "english"
    moods: List[str]

# -------------------------------
# Helper function to save song
def save_song_to_db(song: SongCreate, db: Session) -> Song:
    existing = db.query(Song).filter(Song.title == song.title, Song.artist == song.artist).first()
    if existing:
        return existing

    mood_objs = []
    for name in song.moods:
        mood = db.query(Mood).filter_by(name=name).first()
        if not mood:
            mood = Mood(name=name)
            db.add(mood)
            db.commit()
            db.refresh(mood)
        mood_objs.append(mood)

    db_song = Song(
        title=song.title,
        artist=song.artist,
        album_image=song.album_image,
        spotify_url=song.spotify_url,
        popularity=song.popularity,
        language=song.language,
        moods=mood_objs
    )
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song

# -------------------------------
# 🎵 Save Song (with moods)
@app.get("/")
def read_root():
    return {"message": "Welcome to Moodframe!"}

@app.post("/save_song")
def save_song(song: SongCreate, db: Session = Depends(get_db)):
    saved = save_song_to_db(song, db)
    return {"message": "Song saved", "song": saved}

# -------------------------------
# 🎵 Get Song for a given mood
@app.get("/get_song")
def get_song(mood: str, user_id: str, db: Session = Depends(get_db)):
    mood_obj = db.query(Mood).filter_by(name=mood).first()
    if not mood_obj:
        return {"error": f"No songs found for mood: {mood}"}

    song = (
        db.query(Song)
        .join(Song.moods)
        .filter(Mood.id == mood_obj.id)
        .filter(~Song.id.in_(
            db.query(UserFeedback.song_id).filter_by(user_id=user_id, liked=False)
        ))
        .order_by(Song.popularity.desc())
        .first()
    )

    if not song:
        tracks = get_tracks_for_mood(mood)
        if tracks:
            track = tracks[0]
            song_data = SongCreate(
                title=track["title"],
                artist=track["artist"],
                album_image=track["album_image"],
                spotify_url=track["spotify_url"],
                popularity=track.get("popularity", 50),
                language=track.get("language", "english"),
                moods=[mood]
            )
            song = save_song_to_db(song_data, db)
        else:
            return {"error": "No songs available from Spotify for this mood."}

    return song

# -------------------------------
# 🎵 User Feedback
@app.post("/feedback")
def feedback(user_id: str, song_id: int, liked: bool, db: Session = Depends(get_db)):
    feedback_entry = UserFeedback(user_id=user_id, song_id=song_id, liked=liked)
    db.add(feedback_entry)
    db.commit()
    return {"message": "Feedback recorded"}

# -------------------------------
# 🎵 Optional: Direct Spotify Search Test
@app.get("/songs")
def songs_by_mood(mood: str = Query(..., description="Mood like 'chill', 'melancholic'")):
    track = get_tracks_for_mood(mood)
    if not track:
        raise HTTPException(status_code=404, detail="No track found for this mood.")
    return {"mood": mood, "result": track}
