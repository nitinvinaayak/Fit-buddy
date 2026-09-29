# FitBuddy - AI Fitness Plan Generator

FitBuddy is an AI-powered fitness plan generator that creates a
7-day general wellness workout plan based on user preferences.

## Features

- User details input
- 7-day workout plan generation
- Nutrition and recovery tips
- Feedback-based workout plan updates
- SQLite database storage
- Admin view for registered users
- FastAPI backend
- Jinja2 HTML frontend
- Gemini AI integration

## Technologies Used

- Python
- FastAPI
- Jinja2
- SQLAlchemy
- SQLite
- Google Gemini API
- HTML
- CSS

## Project Structure

```text
FitBuddy-AI/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── schemas.py
│   ├── routes.py
│   ├── gemini_client.py
│   ├── gemini_generator.py
│   ├── gemini_flash_generator.py
│   └── updated_plan.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── result.html
│   ├── all_users.html
│   └── admin_login.html
│
├── static/
│   └── css/
│       └── style.css
│
├── tests/
│   └── test_app.py
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md