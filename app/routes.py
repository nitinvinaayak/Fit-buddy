from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database import (
    User,
    SessionLocal,
    get_all_users,
    get_user_by_id,
    init_db,
    save_user,
    update_user_plan,
)
from app.gemini_flash_generator import generate_nutrition_tip
from app.gemini_generator import generate_workout_plan
from app.schemas import FeedbackRequest, UserInput
from app.updated_plan import generate_updated_plan
from app.config import settings


router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "templates"

templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

# Create database tables when the application starts.
init_db()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "error": None,
        },
    )


@router.post("/generate-workout", response_class=HTMLResponse)
async def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
):
    db = SessionLocal()

    try:
        user_data = UserInput(
            username=username,
            user_id=user_id,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
        )

        workout_plan = generate_workout_plan(
            username=user_data.username,
            age=user_data.age,
            weight=user_data.weight,
            goal=user_data.goal,
            intensity=user_data.intensity,
        )

        nutrition_tip = generate_nutrition_tip(
            username=user_data.username,
            age=user_data.age,
            weight=user_data.weight,
            goal=user_data.goal,
        )

        existing_user = get_user_by_id(
            db,
            user_data.user_id,
        )

        if existing_user:
            existing_user.username = user_data.username
            existing_user.age = user_data.age
            existing_user.weight = user_data.weight
            existing_user.goal = user_data.goal
            existing_user.intensity = user_data.intensity
            existing_user.original_plan = workout_plan
            existing_user.updated_plan = None
            existing_user.nutrition_tip = nutrition_tip
            existing_user.feedback = None

            db.commit()
            db.refresh(existing_user)

            user = existing_user

        else:
            user = User(
                user_id=user_data.user_id,
                username=user_data.username,
                age=user_data.age,
                weight=user_data.weight,
                goal=user_data.goal,
                intensity=user_data.intensity,
                original_plan=workout_plan,
                nutrition_tip=nutrition_tip,
            )

            save_user(db, user)

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": user,
                "username": user.username,
                "user_id": user.user_id,
                "age": user.age,
                "weight": user.weight,
                "goal": user.goal,
                "intensity": user.intensity,
                "workout_plan": user.original_plan,
                "updated_plan": user.updated_plan,
                "nutrition_tip": user.nutrition_tip,
                "feedback": user.feedback,
                "message": None,
                "error": None,
            },
        )

    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": str(exc),
            },
            status_code=500,
        )

    finally:
        db.close()


@router.post("/submit-feedback", response_class=HTMLResponse)
async def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
):
    db = SessionLocal()

    try:
        feedback_data = FeedbackRequest(
            user_id=user_id,
            feedback=feedback,
        )

        user = get_user_by_id(
            db,
            feedback_data.user_id,
        )

        if not user:
            return templates.TemplateResponse(
                request=request,
                name="result.html",
                context={
                    "error": "User not found.",
                    "message": None,
                    "user": None,
                },
                status_code=404,
            )

        if not user.original_plan:
            return templates.TemplateResponse(
                request=request,
                name="result.html",
                context={
                    "error": "No original workout plan was found.",
                    "message": None,
                    "user": user,
                },
                status_code=400,
            )

        revised_plan = generate_updated_plan(
            original_plan=user.original_plan,
            feedback=feedback_data.feedback,
            goal=user.goal,
            intensity=user.intensity,
        )

        update_user_plan(
            db=db,
            user=user,
            updated_plan=revised_plan,
            feedback=feedback_data.feedback,
        )

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": user,
                "username": user.username,
                "user_id": user.user_id,
                "age": user.age,
                "weight": user.weight,
                "goal": user.goal,
                "intensity": user.intensity,
                "workout_plan": user.original_plan,
                "updated_plan": user.updated_plan,
                "nutrition_tip": user.nutrition_tip,
                "feedback": user.feedback,
                "message": "Your workout plan has been updated successfully.",
                "error": None,
            },
        )

    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": None,
                "message": None,
                "error": str(exc),
            },
            status_code=500,
        )

    finally:
        db.close()


@router.get("/view-all-users", response_class=HTMLResponse)
async def view_all_users(
    request: Request,
    key: str | None = None,
):
    if settings.admin_key and key != settings.admin_key:
        return templates.TemplateResponse(
            request=request,
            name="admin_login.html",
            context={
                "error": "Invalid admin key.",
            },
            status_code=401,
        )

    db = SessionLocal()

    try:
        users = get_all_users(db)

        return templates.TemplateResponse(
            request=request,
            name="all_users.html",
            context={
                "users": users,
            },
        )

    finally:
        db.close()


@router.get("/api/users")
async def api_users(
    key: str | None = None,
):
    if settings.admin_key and key != settings.admin_key:
        return {
            "error": "Invalid admin key."
        }

    db = SessionLocal()

    try:
        users = get_all_users(db)

        return {
            "users": [
                {
                    "id": user.id,
                    "user_id": user.user_id,
                    "username": user.username,
                    "age": user.age,
                    "weight": user.weight,
                    "goal": user.goal,
                    "intensity": user.intensity,
                    "original_plan": user.original_plan,
                    "updated_plan": user.updated_plan,
                    "nutrition_tip": user.nutrition_tip,
                    "feedback": user.feedback,
                }
                for user in users
            ]
        }

    finally:
        db.close()