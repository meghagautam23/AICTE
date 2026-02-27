from flask import Blueprint, current_app, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from mindease import db
from mindease.models import ChatMessage
from mindease.services import (
    EMERGENCY_NOTE,
    analyze_sentiment,
    detect_repeated_negative_sentiment,
    generate_chat_reply,
)


chat_bp = Blueprint("chat", __name__, url_prefix="/chat")


@chat_bp.route("/")
@login_required
def chat_room():
    user_conversation = (
        ChatMessage.query.filter_by(user_id=current_user.id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )
    return render_template("chat.html", messages=user_conversation)


@chat_bp.route("/send", methods=["POST"])
@login_required
def send_message():
    payload = request.get_json(silent=True) or {}
    user_message = payload.get("message", "").strip()

    if not user_message:
        user_message = request.form.get("message", "").strip()

    if not user_message:
        if request.is_json:
            return jsonify({"error": "Message cannot be empty."}), 400
        return redirect(url_for("chat.chat_room"))

    sentiment_score, sentiment_label = analyze_sentiment(user_message)
    bot_reply = generate_chat_reply(user_message, sentiment_label)

    chat_record = ChatMessage(
        user_id=current_user.id,
        user_text=user_message,
        bot_reply=bot_reply,
        sentiment_score=sentiment_score,
        sentiment_label=sentiment_label,
    )

    db.session.add(chat_record)
    db.session.commit()

    threshold = current_app.config.get("NEGATIVE_STREAK_THRESHOLD", 3)
    should_suggest_emergency = detect_repeated_negative_sentiment(current_user.id, threshold)

    if should_suggest_emergency:
        bot_reply = f"{bot_reply} {EMERGENCY_NOTE}"
        chat_record.bot_reply = bot_reply
        db.session.commit()

    if request.is_json:
        return jsonify(
            {
                "user_text": user_message,
                "bot_reply": bot_reply,
                "sentiment_label": sentiment_label,
                "sentiment_score": sentiment_score,
                "emergency_prompt": should_suggest_emergency,
                "created_at": chat_record.created_at.strftime("%I:%M %p"),
            }
        )

    return redirect(url_for("chat.chat_room"))
