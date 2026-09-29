from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routes import router


app = FastAPI(
    title=settings.app_name,
    description="AI-powered fitness plan generator using Gemini.",
    version="1.0.0",
)

# Serve CSS and other static files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)

# Register application routes
app.include_router(router)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.app_name,
    }