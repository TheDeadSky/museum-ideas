from contextlib import asynccontextmanager

import sentry_sdk

from fastapi import (
    FastAPI,
    Depends
)
from sqlalchemy import text
from sqlalchemy.orm import Session

from config import settings
from db.database import get_db, create_tables
from modules import (
    registration,
    self_support_course,
    feedback,
    share_experience,
    history,
    common
)

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

app.include_router(self_support_course.routes.router)
app.include_router(registration.routes.router)
app.include_router(feedback.routes.router)
app.include_router(share_experience.routes.router)
app.include_router(history.routes.router)
app.include_router(common.routes.router)


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}
