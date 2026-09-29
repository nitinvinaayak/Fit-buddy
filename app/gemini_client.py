from google import genai
from google.genai import types

from app.config import settings


# Models to try one by one
FALLBACK_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-2.5-flash",
]


def generate_with_gemini(prompt: str, model: str) -> str:
    """
    Send a prompt to Gemini.

    If the selected model is temporarily unavailable,
    try the fallback models one by one.

    If all models fail, return a friendly message
    instead of showing a technical error to the user.
    """

    if not settings.gemini_api_key:
        raise RuntimeError(
            "Gemini API key is not configured. "
            "Please add GEMINI_API_KEY to the .env file."
        )

    client = genai.Client(
        api_key=settings.gemini_api_key
    )

    # Start with the model requested by the application
    models_to_try = [model]

    # Add fallback models without duplicates
    for fallback_model in FALLBACK_MODELS:
        if fallback_model not in models_to_try:
            models_to_try.append(fallback_model)

    last_error = None

    for current_model in models_to_try:
        try:
            response = client.models.generate_content(
                model=current_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=5000,
                ),
            )

            if response.text:
                return response.text.strip()

        except Exception as error:
            last_error = error
            print(
                f"Gemini model '{current_model}' failed: {error}"
            )

    # Friendly message if all models fail
    print(f"All Gemini models failed. Last error: {last_error}")

    return """
Sorry! Our AI service is temporarily busy.

We could not generate your fitness plan right now.
Please wait a few minutes and try again.

Your information has not been lost. ❤️
"""

