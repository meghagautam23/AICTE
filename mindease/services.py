import random
from collections import defaultdict
from datetime import datetime, timedelta, timezone

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from mindease.models import ChatMessage, MoodEntry
from mindease.time_utils import get_app_timezone, local_now, to_local


sentiment_analyzer = SentimentIntensityAnalyzer()


EMERGENCY_NOTE = (
    "I am noticing a pattern of distress in your recent updates. "
    "Please consider reaching out to immediate support: call or text 988 "
    "(Suicide & Crisis Lifeline) or contact campus counseling services."
)


MOTIVATIONAL_QUOTES = [
    "Progress is built from small steps repeated consistently.",
    "You are allowed to pause, breathe, and start again.",
    "Asking for help is a strength, not a setback.",
    "Your effort today matters, even if it feels imperfect.",
    "Healing is not linear, but every step still counts.",
    "Rest is productive when your mind needs recovery.",
    "You have survived difficult days before, and that resilience is real.",
]


MOOD_SCORE_HINTS = {
    "Very Happy": 0.75,
    "Happy": 0.45,
    "Okay": 0.05,
    "Anxious": -0.25,
    "Sad": -0.45,
    "Overwhelmed": -0.7,
}


NEGATIVE_RESPONSE_LIBRARY = [
    "That sounds heavy right now. Let's break this moment into one manageable step. Start with a 60-second breathing pause.",
    "Thank you for sharing honestly. If your mind is racing, write down the top two stressors and tackle only one first.",
    "I hear you. Try this reset: drink water, move your body for two minutes, then return to the next small task.",
]


NEUTRAL_RESPONSE_LIBRARY = [
    "Thanks for checking in. Keeping track of your feelings regularly can reveal useful patterns for your week.",
    "You're doing the right thing by reflecting. What is one thing that feels manageable in the next hour?",
    "Let's keep momentum: choose one task for now, and give yourself credit when it's done.",
]


POSITIVE_RESPONSE_LIBRARY = [
    "Great to hear a positive note from you. Keep reinforcing what worked today.",
    "That is a strong update. Consider journaling what helped so you can repeat it during tougher moments.",
    "Nice progress. Celebrating small wins is a proven way to build emotional resilience.",
]


def analyze_sentiment(text):
    cleaned_text = (text or "").strip()
    if not cleaned_text:
        return 0.0, "neutral"

    # VADER returns a normalized compound score in [-1, 1].
    sentiment_score = sentiment_analyzer.polarity_scores(cleaned_text)["compound"]

    if sentiment_score <= -0.2:
        sentiment_label = "negative"
    elif sentiment_score >= 0.2:
        sentiment_label = "positive"
    else:
        sentiment_label = "neutral"

    return sentiment_score, sentiment_label


def generate_chat_reply(user_message, sentiment_label):
    lowered_message = user_message.lower()

    if "exam" in lowered_message or "deadline" in lowered_message:
        study_tip = "A focused 25-minute study sprint followed by a short break can lower overwhelm quickly."
    elif "sleep" in lowered_message or "tired" in lowered_message:
        study_tip = "Sleep is mental recovery. A consistent bedtime routine can improve stress tolerance the next day."
    else:
        study_tip = "Consistency beats intensity. Prioritize one small healthy action and repeat it daily."

    if sentiment_label == "negative":
        base_response = random.choice(NEGATIVE_RESPONSE_LIBRARY)
    elif sentiment_label == "positive":
        base_response = random.choice(POSITIVE_RESPONSE_LIBRARY)
    else:
        base_response = random.choice(NEUTRAL_RESPONSE_LIBRARY)

    return f"{base_response} {study_tip}"


def pick_motivational_quote():
    return random.choice(MOTIVATIONAL_QUOTES)


def infer_sentiment_from_mood(mood_label):
    score = MOOD_SCORE_HINTS.get(mood_label, 0.0)
    if score <= -0.2:
        return score, "negative"
    if score >= 0.2:
        return score, "positive"
    return score, "neutral"


def detect_repeated_negative_sentiment(user_id, threshold):
    recent_chats = (
        ChatMessage.query.filter_by(user_id=user_id)
        .order_by(ChatMessage.created_at.desc())
        .limit(threshold)
        .all()
    )
    recent_moods = (
        MoodEntry.query.filter_by(user_id=user_id)
        .order_by(MoodEntry.created_at.desc())
        .limit(threshold)
        .all()
    )

    # Merge both interaction types to check recent emotional trajectory holistically.
    merged_events = []
    merged_events.extend(
        [(entry.created_at, entry.sentiment_label) for entry in recent_chats]
    )
    merged_events.extend(
        [(entry.created_at, entry.sentiment_label) for entry in recent_moods]
    )

    merged_events.sort(key=lambda item: item[0], reverse=True)
    latest_events = merged_events[:threshold]

    if len(latest_events) < threshold:
        return False

    return all(label == "negative" for _, label in latest_events)


def build_weekly_mood_summary(user_id, days=7):
    today = local_now().date()
    start_date = today - timedelta(days=days - 1)

    timezone_info = get_app_timezone()
    start_local = datetime.combine(start_date, datetime.min.time(), tzinfo=timezone_info)
    start_utc_naive = start_local.astimezone(timezone.utc).replace(tzinfo=None)

    weekly_entries = (
        MoodEntry.query.filter(
            MoodEntry.user_id == user_id,
            MoodEntry.created_at >= start_utc_naive,
        )
        .order_by(MoodEntry.created_at.asc())
        .all()
    )

    date_labels = []
    daily_score_buckets = defaultdict(list)
    mood_distribution = defaultdict(int)

    # Prebuild day labels so chart columns remain stable even when a day has no logs.
    for day_index in range(days):
        current_day = start_date + timedelta(days=day_index)
        date_labels.append(current_day.strftime("%a"))

    for entry in weekly_entries:
        day_key = to_local(entry.created_at).date()
        daily_score_buckets[day_key].append(entry.sentiment_score)
        mood_distribution[entry.mood_label] += 1

    daily_avg_scores = []
    for day_index in range(days):
        day_key = start_date + timedelta(days=day_index)
        scores = daily_score_buckets.get(day_key, [])
        daily_avg_scores.append(round(sum(scores) / len(scores), 2) if scores else 0)

    all_scores = [entry.sentiment_score for entry in weekly_entries]
    weekly_average = round(sum(all_scores) / len(all_scores), 2) if all_scores else 0
    dominant_mood = max(mood_distribution, key=mood_distribution.get) if mood_distribution else "N/A"

    return {
        "total_entries": len(weekly_entries),
        "weekly_average": weekly_average,
        "dominant_mood": dominant_mood,
        "date_labels": date_labels,
        "daily_avg_scores": daily_avg_scores,
        "mood_distribution": dict(mood_distribution),
    }
