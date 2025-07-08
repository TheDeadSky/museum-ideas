from contextlib import asynccontextmanager
import logging
import aiohttp
from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Query
)
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from schemas import BaseResponse, CourseNotificationResponse
from config import settings
from db.database import get_db, create_tables
from services.registration import registration, RegistrationException, is_user_registered
from services.history import get_random_history, HistoryException
from services.self_support_course.schemas import SelfSupportCourseResponse, CourseUserAnswer
from services.registration.schemas import RegistrationData, RegistrationResponse
from services.self_support_course.actions import load_self_support_course, save_self_support_course_answer
from services.share_experience.actions import save_user_experience
from services.share_experience.schemas import ShareExperienceData
from services.feedback.actions import answer_feedback, get_feedbacks, render_feedbacks_page, save_user_feedback
from services.feedback.schemas import FeedbackAnswerData, FeedbackListResponse, IncomingFeedback
from db.models import User, UserCourseProgress


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
async def send_feedback(feedback: IncomingFeedback, db: Session = Depends(get_db)) -> BaseResponse:
    """Send feedback to the museum"""

    return await save_user_feedback(feedback, db)


@app.get("/admin/feedbacks", response_class=HTMLResponse)
async def feedbacks_page(key: str = Query(default="")):
    """Get feedbacks page"""

    logging.info(key)

    if key == "sHHUc6u3VTgP*WSu1vz^p@8zC!Y":
        return await render_feedbacks_page()

    raise HTTPException(status_code=404, detail="Not found")


@app.get("/feedback/list")
async def get_feedbacks_list(
    page: int = 1,
    per_page: int = 10,
    search: str = "",
    status: str = "pending",
    db: Session = Depends(get_db)
) -> FeedbackListResponse:
    """Get feedbacks list"""
    print("page, per_page, search, status", page, per_page, search, status)
    return await get_feedbacks(db, page, per_page, search, status)


@app.post("/feedback/answer")
async def answer_feedback_endpoint(answer_data: FeedbackAnswerData, db: Session = Depends(get_db)) -> BaseResponse:
    """Answer feedback"""

    return await answer_feedback(answer_data, db)


@app.post("/share-experience")
async def share_experience(data: ShareExperienceData, db: Session = Depends(get_db)) -> BaseResponse:
    return await save_user_experience(data, db)


@app.post("/notify-users-about-course")
async def new_course_part_notification(db: Session = Depends(get_db)) -> CourseNotificationResponse:
    """Get users telegram IDs split by course progress status"""

    try:
        # Get users with course progress
        users_with_progress_query = select(User.telegram_id).distinct().join(
            UserCourseProgress, User.id == UserCourseProgress.user_id
        ).where(User.telegram_id.isnot(None))

        users_with_progress = db.execute(users_with_progress_query).scalars().all()
        users_with_progress_ids = [str(tg_id) for tg_id in users_with_progress if tg_id]

        # Get users without course progress but subscribed to a course
        users_without_progress_query = select(User.telegram_id).where(
            and_(
                User.telegram_id.isnot(None),
                ~User.id.in_(
                    select(UserCourseProgress.user_id).distinct()
                )
            )
        )

        users_without_progress = db.execute(users_without_progress_query).scalars().all()
        users_without_progress_ids = [str(tg_id) for tg_id in users_without_progress if tg_id]

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://museum_bot:9000/api/notify-users-about-course",
                json={
                    "users_with_progress": users_with_progress_ids,
                    "users_without_progress": users_without_progress_ids
                }
            ) as response:
                response_data = await response.json()

        if response_data.get("success"):
            return CourseNotificationResponse(
                success=True,
                message=(
                    f"Found {len(users_with_progress_ids)} users with progress and "
                    f"{len(users_without_progress_ids)} users without progress"
                )
            )
        else:
            return CourseNotificationResponse(
                success=False,
                message=response_data.get("message")
            )

    except Exception as e:
        return CourseNotificationResponse(
            success=False,
            message=f"Error getting user notifications: {str(e)}"
        )
