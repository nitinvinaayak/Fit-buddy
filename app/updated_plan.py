from app.config import settings
from app.gemini_client import generate_with_gemini


def generate_updated_plan(
    original_plan: str,
    feedback: str,
    goal: str,
    intensity: str,
) -> str:
    prompt = f"""
You are FitBuddy, an AI fitness planning assistant.

The user has an existing 7-day workout plan and has provided feedback.

Fitness Goal:
{goal}

Workout Intensity:
{intensity}

Original Plan:
{original_plan}

User Feedback:
{feedback}

Create an updated 7-day workout plan based on the user's feedback.

Requirements:
1. Keep the plan safe and practical.
2. Keep the user's fitness goal in mind.
3. Adjust exercises, duration, difficulty, or rest
   according to the feedback.
4. Include Day 1 through Day 7.
5. Include warm-up and cool-down suggestions.
6. Include recovery/rest where appropriate.
7. Do not recommend extreme exercise, fasting,
   starvation, rapid weight loss, supplements,
   or unsafe activities.
8. Do not provide medical diagnoses.
9. If the user reports pain, dizziness, or feeling unwell,
   recommend stopping the activity and seeking appropriate
   adult/professional help.
10. Keep the language simple and easy to understand.

Use this format:

UPDATED FITBUDDY 7-DAY WORKOUT PLAN

Day 1:
- Warm-up:
- Workout:
- Cool-down:

Day 2:
- Warm-up:
- Workout:
- Cool-down:

Continue through Day 7.

At the end, include:
CHANGES BASED ON FEEDBACK
- Briefly explain what was adjusted.
"""

    return generate_with_gemini(
        prompt=prompt,
        model=settings.workout_model,
    )