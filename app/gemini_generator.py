from app.config import settings
from app.gemini_client import generate_with_gemini


def generate_workout_plan(
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
) -> str:
    prompt = f"""
You are FitBuddy, an AI fitness planning assistant.

Create a safe and practical 7-day general fitness plan for the following user:

Name: {username}
Age: {age}
Weight: {weight} kg
Fitness Goal: {goal}
Workout Intensity: {intensity}

Requirements:
1. Create a plan for Day 1 through Day 7.
2. Include warm-up and cool-down suggestions.
3. Include suitable exercises, sets/repetitions or duration.
4. Include rest or recovery days where appropriate.
5. Keep the plan beginner-friendly and practical.
6. Do not recommend extreme exercise, fasting, starvation,
   rapid weight loss, supplements, or unsafe activities.
7. Do not make medical diagnoses.
8. Give general wellness guidance only.
9. Remind the user to stop if they feel pain, dizziness,
   or feel unwell and seek appropriate adult/professional help.
10. Keep the response easy to read.

Use this format:

FITBUDDY 7-DAY WORKOUT PLAN

Day 1:
- Warm-up:
- Workout:
- Cool-down:

Day 2:
- Warm-up:
- Workout:
- Cool-down:

Continue through Day 7.

At the end, add:
GENERAL SAFETY NOTES
- A short list of safe exercise reminders.
"""

    return generate_with_gemini(
        prompt=prompt,
        model=settings.workout_model,
    )