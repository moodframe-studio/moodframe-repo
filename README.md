# 🎵 MoodFrame Studio

AI-powered backend to recommend songs based on the mood extracted from images, with Spotify API integration and user feedback tracking.

---

## 🚀 Features

- 🧠 AI image analysis using CLIP to detect mood
- 🎧 Spotify integration via Spotipy to fetch tracks
- 🔁 Dynamic song recommendation logic with feedback learning
- 🎯 Filtered results to avoid repeating rejected songs
- 🗂️ SQLAlchemy models with many-to-many `Song <-> Mood` relationships
- 📦 REST API using FastAPI
- ☁️ Ready for deployment on Render.com

---

## 🛠️ Tech Stack

- **FastAPI** - API framework
- **SQLAlchemy** - ORM for PostgreSQL
- **Spotipy** - Spotify API client
- **Transformers / CLIP** - Mood analysis from images
- **PostgreSQL** - Database
- **Uvicorn** - ASGI server
- **Python-dotenv** - Manage environment variables

---

## 🔧 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/moodframe-studio.git
cd moodframe-studio
