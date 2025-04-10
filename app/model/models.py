from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

# Timestamp mixin for created_at and updated_at
class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# Association table for many-to-many relationship between songs and moods
song_mood_association = Table(
    'song_mood_association',
    Base.metadata,
    Column('song_id', Integer, ForeignKey('songs.id')),
    Column('mood_id', Integer, ForeignKey('moods.id'))
)


class Song(Base, TimestampMixin):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    artist = Column(String)
    album_image = Column(String)
    spotify_url = Column(String)
    popularity = Column(Integer)
    rejected = Column(Boolean, default=False)
    selected = Column(Boolean, default=True)
    language = Column(String)

    moods = relationship("Mood", secondary=song_mood_association, back_populates="songs")


class Mood(Base, TimestampMixin):
    __tablename__ = "moods"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    songs = relationship("Song", secondary=song_mood_association, back_populates="moods")


class UserFeedback(Base, TimestampMixin):
    __tablename__ = "user_feedback"

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    song_id = Column(Integer)
    liked = Column(Boolean)  # True if user selected it, False if rejected
