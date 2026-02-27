# MindEase - AI Emotional Wellness Companion for Students

MindEase is a production-style Flask web application focused on student emotional wellness. It combines mood tracking, sentiment-aware journaling, and an AI-style support chat interface to help students monitor emotional trends and receive timely guidance.

## Project Description
MindEase is designed as an internship-ready mental wellness platform that goes beyond a basic chatbot by providing:
- User authentication and personalized dashboards
- Mood logging with sentiment analysis
- Chat history per user
- Repeated negative sentiment detection with emergency support suggestion
- Weekly emotional trend visualization
- Motivational quote generator

This project emphasizes clean architecture, modular code organization, and professional documentation.

## Key Features
1. Login/signup authentication using secure password hashing
2. Mood tracking with SQLite persistence
3. Sentiment analysis (VADER) for mood notes and chat messages
4. Emergency contact suggestion when repeated negative sentiment is detected
5. Weekly mood summary dashboard
6. Motivational quote generator
7. Per-user chat history storage
8. Additional pages: About, Resources, FAQ
9. Fully responsive, modern glassmorphism user interface

## UI/UX Highlights
- Purple-blue gradient visual identity
- Glassmorphism cards and panels
- Animated chat bubbles
- Sidebar-based navigation (Dashboard, Chat, Mood Log, Resources)
- Mobile-friendly responsive behavior
- Micro-interactions on cards, buttons, and chart elements

## Architecture Explanation
MindEase follows a Flask app factory + blueprint architecture for scalability.

### Backend Structure
- `app.py`: Entry point
- `config.py`: Central configuration (SQLite URI, sentiment thresholds, mood options)
- `mindease/__init__.py`: App factory, extension initialization, blueprint registration
- `mindease/models/`: SQLAlchemy models for users, mood entries, and chat history
- `mindease/routes/`: Blueprints separated by concern (`auth`, `main`, `chat`, `mood`, `pages`)
- `mindease/services.py`: Business logic for sentiment scoring, weekly summaries, quote generation, and emergency detection

### Data Layer
SQLite stores:
- `users`
- `mood_entries`
- `chat_messages`

Each record is linked to its user through foreign keys for personalized tracking.

### Frontend Layer
- Jinja templating with reusable base layout
- Separate static assets (`static/css/style.css`, `static/js/*.js`)
- AJAX-based chat updates for smoother interaction

## Tech Stack
- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Login
- SQLite
- VADER Sentiment Analyzer (`vaderSentiment`)
- HTML5, CSS3, JavaScript (vanilla)
- Jinja2 templating

## Folder Structure
```text
Mental_Health_Chatbot-main/
|-- app.py
|-- config.py
|-- requirements.txt
|-- README.md
|-- mindease/
|   |-- __init__.py
|   |-- services.py
|   |-- models/
|   |   |-- __init__.py
|   |   |-- user.py
|   |   |-- mood_entry.py
|   |   `-- chat_message.py
|   |-- routes/
|   |   |-- __init__.py
|   |   |-- auth.py
|   |   |-- main.py
|   |   |-- chat.py
|   |   |-- mood.py
|   |   `-- pages.py
|   |-- templates/
|   |   |-- base.html
|   |   |-- index.html
|   |   |-- dashboard.html
|   |   |-- chat.html
|   |   |-- mood_log.html
|   |   |-- about.html
|   |   |-- resources.html
|   |   |-- faq.html
|   |   `-- auth/
|   |       |-- login.html
|   |       `-- signup.html
|   `-- static/
|       |-- css/style.css
|       `-- js/
|           |-- main.js
|           `-- chat.js
```

## Setup and Run
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask app:
   ```bash
   python app.py
   ```
4. Open in browser:
   - `http://127.0.0.1:5050/`

Optional:
- Set a custom port with `PORT`, for example:
  ```bash
  PORT=8000 python app.py
  ```

`mindease.db` is created automatically on first run.

## Future Enhancements
1. Role-based admin analytics panel
2. OAuth login (Google/Microsoft campus accounts)
3. PDF export for weekly emotional reports
4. Email reminders for daily mood check-ins
5. LLM integration for richer conversational assistance
6. Stronger crisis detection with multi-signal risk scoring
7. Unit/integration test suite with CI pipeline

