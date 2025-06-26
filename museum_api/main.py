from contextlib import asynccontextmanager
from fastapi import (
    FastAPI,
    Depends,
    HTTPException
)
from sqlalchemy.orm import Session
from datetime import datetime

from db.models import Course, CoursePart, UserCourseProgress
from db.utils import get_user_by_sm_id
from services.registration import registration, RegistrationException, is_user_registered
from services.history import get_random_history, HistoryException
from schemas import (
    Feedback,
    SelfSupportCourseData,
    RegistrationData,
    RegistrationResponse,
    SelfSupportCoursePartData,
    SelfSupportCourseResponse,
    CourseUserAnswer,
    BaseResponse
)
from config import settings
from db.database import get_db, create_tables


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
        # Test database connection
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
    user = get_user_by_sm_id(db, sm_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User not found by sm_id({sm_id})")

    course = db.query(Course).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    user_progress = db.query(UserCourseProgress).filter(
        UserCourseProgress.user_id == user.id
    ).order_by(UserCourseProgress.date.desc()).first()

    if not user_progress:
        next_course_part = db.query(CoursePart).filter(
            CoursePart.course_id == course.id
        ).order_by(CoursePart.order_number).first()

    else:
        finished_course_part = db.query(CoursePart).filter(
            CoursePart.course_id == course.id,
            CoursePart.id == user_progress.part_id
        ).first()

        next_course_part = db.query(CoursePart).filter(
            CoursePart.course_id == course.id,
            CoursePart.order_number == finished_course_part.order_number + 1,
        ).first()

    if next_course_part.date_of_publication > datetime.now():
        return BaseResponse(
            success=False,
            message=f"Следующая лекция выйдет {next_course_part.date_of_publication.strftime('%d.%m.%Y')}"
        )

    if not next_course_part:
        raise HTTPException(status_code=404, detail="No course parts found")

    course_data = SelfSupportCourseData(
        id=course.id,
        title=course.course_name,
        description=course.description
    )

    part_data = SelfSupportCoursePartData(
        id=next_course_part.id,
        title=next_course_part.title,
        description=next_course_part.description,
        video_url=next_course_part.video_url,
        image_url=next_course_part.image_url,
        course_text=next_course_part.description,
        question=next_course_part.question,
        publication_date=next_course_part.date_of_publication
    )

    self_support_course_schema = SelfSupportCourseResponse(
        success=True,
        message="Начата новая часть курса",
        course_data=course_data,
        part_data=part_data
    )

    return self_support_course_schema


@app.post("/self-support-course/{sm_id}/answer")
async def answer_self_support_course(
    answer_data: CourseUserAnswer,
    db: Session = Depends(get_db)
) -> SelfSupportCourseResponse:
    """Answer a self-support course question"""
    user = get_user_by_sm_id(db, answer_data.sm_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User not found by sm_id({answer_data.sm_id})")

    user_progress = UserCourseProgress(
        user_id=user.id,
        part_id=answer_data.part_id,
        answer=answer_data.answer
    )
    db.add(user_progress)
    db.commit()

    return BaseResponse(
        success=True,
        message="Ответ сохранен"
    )


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
async def send_feedback(feedback: Feedback, db: Session = Depends(get_db)) -> Feedback:
    """Send feedback to the museum"""

    # TODO: Save feedback to database
    return feedback
