from contextlib import asynccontextmanager
from fastapi import (
    FastAPI,
    Depends,
    HTTPException
)
from sqlalchemy.orm import Session

from schemas import BaseResponse
from config import settings
from db.database import get_db, create_tables
from services.registration import registration, RegistrationException, is_user_registered
from services.history import get_random_history, HistoryException
from services.self_support_course.schemas import SelfSupportCourseResponse, CourseUserAnswer
from services.registration.schemas import RegistrationData, RegistrationResponse
from services.self_support_course.actions import load_self_support_course, save_self_support_course_answer
from services.share_experience.actions import save_user_experience
from services.share_experience.schemas import ShareExperienceData
from services.feedback.actions import save_user_feedback
from services.feedback.schemas import Feedback


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


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}


@app.post("/self-support-course/{sm_id}")
async def get_self_support_course(
    sm_id: str,
    db: Session = Depends(get_db)
) -> SelfSupportCourseResponse:
    """Get a self-support course for a user"""
    self_support_course = await load_self_support_course(sm_id, db)

    return self_support_course


@app.post("/self-support-course/{sm_id}/answer")
async def answer_self_support_course(
    answer_data: CourseUserAnswer,
    db: Session = Depends(get_db)
) -> SelfSupportCourseResponse:
    """Answer a self-support course question"""
    return await save_self_support_course_answer(answer_data, db)


@app.post("/register")
async def register(registration_data: RegistrationData, db: Session = Depends(get_db)) -> RegistrationResponse:
    """Register a new user"""
    try:
        return await registration(registration_data, db)
    except RegistrationException as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {e}")


@app.get("/is-registered/{sm_id}")
async def is_registered(sm_id: str, db: Session = Depends(get_db)) -> RegistrationResponse:
    """Check if a user is registered by email"""
    return await is_user_registered(sm_id, db)


@app.get("/random-history/{sm_id}")
async def get_random_history_endpoint(sm_id: str, db: Session = Depends(get_db)):
    """Get a random unseen story for a user"""
    try:
        return await get_random_history(sm_id, db)
    except HistoryException as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/send-feedback")
async def send_feedback(feedback: Feedback, db: Session = Depends(get_db)) -> BaseResponse:
    """Send feedback to the museum"""

    return await save_user_feedback(feedback, db)


@app.post("/share-experience")
async def share_experience(data: ShareExperienceData, db: Session = Depends(get_db)) -> BaseResponse:
    return await save_user_experience(data, db)
