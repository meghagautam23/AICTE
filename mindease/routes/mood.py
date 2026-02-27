from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from mindease import db
from mindease.models import MoodEntry
from mindease.services import (
    EMERGENCY_NOTE,
    analyze_sentiment,
    build_weekly_mood_summary,
    detect_repeated_negative_sentiment,
    infer_sentiment_from_mood,
)


mood_bp = Blueprint("mood", __name__, url_prefix="/mood")


@mood_bp.route("/", methods=["GET", "POST"])
@login_required
def mood_log():
    mood_choices = current_app.config.get("MOOD_CHOICES", [])

    if request.method == "POST":
        selected_mood = request.form.get("mood_label", "").strip()
        notes = request.form.get("notes", "").strip()

        if selected_mood not in mood_choices:
            flash("Please choose a valid mood option.", "danger")
            return redirect(url_for("mood.mood_log"))

        if notes:
            sentiment_score, sentiment_label = analyze_sentiment(notes)
        else:
            sentiment_score, sentiment_label = infer_sentiment_from_mood(selected_mood)

        new_entry = MoodEntry(
            user_id=current_user.id,
            mood_label=selected_mood,
            notes=notes,
            sentiment_score=sentiment_score,
            sentiment_label=sentiment_label,
        )

        db.session.add(new_entry)
        db.session.commit()

        streak_limit = current_app.config.get("NEGATIVE_STREAK_THRESHOLD", 3)
        if detect_repeated_negative_sentiment(current_user.id, streak_limit):
            flash(EMERGENCY_NOTE, "warning")

        flash("Mood entry saved successfully.", "success")
        return redirect(url_for("mood.mood_log"))

    entries = (
        MoodEntry.query.filter_by(user_id=current_user.id)
        .order_by(MoodEntry.created_at.desc())
        .limit(30)
        .all()
    )

    weekly_summary = build_weekly_mood_summary(
        current_user.id,
        days=current_app.config.get("WEEKLY_WINDOW_DAYS", 7),
    )

    return render_template(
        "mood_log.html",
        mood_choices=mood_choices,
        mood_entries=entries,
        weekly_summary=weekly_summary,
    )
