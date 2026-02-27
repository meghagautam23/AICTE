import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'mindease.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    NEGATIVE_STREAK_THRESHOLD = 3
    WEEKLY_WINDOW_DAYS = 7
    MOOD_CHOICES = [
        "Very Happy",
        "Happy",
        "Okay",
        "Anxious",
        "Sad",
        "Overwhelmed",
    ]
