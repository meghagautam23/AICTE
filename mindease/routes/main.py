from flask import Blueprint, jsonify, redirect, render_template, url_for
from flask_login import current_user, login_required

from mindease.models import ChatMessage, MoodEntry
from mindease.services import (
    build_weekly_mood_summary,
    pick_motivational_quote,
)


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("index.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    weekly_summary = build_weekly_mood_summary(current_user.id)

    recent_mood_entries = (
        MoodEntry.query.filter_by(user_id=current_user.id)
        .order_by(MoodEntry.created_at.desc())
        .limit(5)
        .all()
    )
    recent_chat_entries = (
        ChatMessage.query.filter_by(user_id=current_user.id)
        .order_by(ChatMessage.created_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "dashboard.html",
        weekly_summary=weekly_summary,
        initial_quote=pick_motivational_quote(),
        recent_mood_entries=recent_mood_entries,
        recent_chat_entries=recent_chat_entries,
    )


@main_bp.route("/quote")
@login_required
def quote_api():
    return jsonify({"quote": pick_motivational_quote()})
