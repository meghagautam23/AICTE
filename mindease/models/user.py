from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from mindease import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    mood_entries = db.relationship(
        "MoodEntry", backref="owner", lazy=True, cascade="all, delete-orphan"
    )
    chat_messages = db.relationship(
        "ChatMessage", backref="owner", lazy=True, cascade="all, delete-orphan"
    )

    def set_password(self, raw_password):
        # Use PBKDF2 for compatibility with Python builds that do not expose hashlib.scrypt.
        self.password_hash = generate_password_hash(
            raw_password, method="pbkdf2:sha256", salt_length=16
        )

    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)
