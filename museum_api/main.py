from contextlib import asynccontextmanager

import sentry_sdk

from fastapi import (
    FastAPI,
    Depends
)
from sqlalchemy.orm import Session

from config import settings
from db.database import get_db, create_tables
from services.self_support_course.routes import router as self_support_course_router
from services.registration.routes import router as registration_router
from services.feedback.routes import router as feedback_router
from services.share_experience.routes import router as share_experience_router
from services.history.routes import router as history_router

sentry_sdk.init("https://9485268e8cff4009a5e148f812472fad@errors.asarta.ru/12", environment="museum_api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for FastAPI"""
    # Startup
    create_tables()
    yield
    # Shutdown (if needed)


app = FastAPI(
    title=settings.APP_NAME,
    description="A museum bot backend API",
    version=settings.APP_VERSION,
    lifespan=lifespan
)

app.include_router(self_support_course_router)
app.include_router(registration_router)
app.include_router(feedback_router)
app.include_router(share_experience_router)
app.include_router(history_router)


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}
