from datetime import datetime

from mindease import db


class ChatMessage(db.Model):
    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    user_text = db.Column(db.Text, nullable=False)
    bot_reply = db.Column(db.Text, nullable=False)
    sentiment_score = db.Column(db.Float, nullable=False, default=0.0)
    sentiment_label = db.Column(db.String(20), nullable=False, default="neutral")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
