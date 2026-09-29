from app.config import settings
from app.gemini_client import generate_with_gemini


def generate_nutrition_tip(
    username: str,
    age: int,
    weight: float,
    goal: str,
) -> str:
    prompt = f"""
You are FitBuddy, a general wellness assistant.

Provide a short, safe nutrition and recovery tip for:

Name: {username}
Age: {age}
Weight: {weight} kg
Fitness Goal: {goal}

Requirements:
1. Give practical general wellness advice.
2. Encourage balanced meals, regular hydration,
   adequate sleep, and recovery.
3. Do not recommend extreme dieting, fasting,
   starvation, diet pills, or supplements.
4. Do not prescribe a specific medical diet.
5. Keep the answer to 2-4 short sentences.
6. Use simple language suitable for a student.
"""

    return generate_with_gemini(
        prompt=prompt,
        model=settings.nutrition_model,
    )