# app/reset_feedback.py
from model.database import SessionLocal
from model.models import UserFeedback

def reset_feedback():
    session = SessionLocal()
    session.query(UserFeedback).delete()
    session.commit()
    session.close()

if __name__ == "__main__":
    reset_feedback()
