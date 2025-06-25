import json
import random
from typing import Annotated, List
from contextlib import asynccontextmanager
from fastapi import (
    FastAPI,
    HTTPException,
    Query,
    Response,
    Depends
)
from sqlalchemy.orm import Session

from db.models import Course, CoursePart, Story, StoryHistory, User
from services.registration.actions import registration
from services.registration.exceptions import RegistrationException
from schemas import (
    Feedback,
    HistoryData,
    HistoryResponse,
    SelfSupportCourse,
    SelfSupportCourseBeginnerData,
    RegistrationData,
    RegistrationResponse
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


@app.get("/")
async def index():
    return {"message": "Hello World from FastAPI"}


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        # Test database connection
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}


@app.get("/get-bot-text")
async def bot_text(keys: Annotated[List[str], Query(max_length=100)]):
    with open("db_imitation/bot_texts.json", "r", encoding="utf-8") as f:
        bot_texts = json.load(f)

    for key in keys:
        if key not in bot_texts:
            return Response(status_code=404, content={"error": f"Key {key} not found in bot_texts"})

    return {key: bot_texts[key] for key in keys}


@app.post("/begin-self-support-course")
async def begin_self_support_course(
    beginner_data: SelfSupportCourseBeginnerData,
    db: Session = Depends(get_db)
) -> SelfSupportCourse:
    course = db.query(Course).filter(Course.id == beginner_data.user_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    first_part = db.query(CoursePart).filter(
        CoursePart.course_id == course.id
    ).order_by(CoursePart.order_number).first()

    if not first_part:
        raise HTTPException(status_code=404, detail="No course parts found")

    self_support_course = {
        "title": course.course_name,
        "description": course.description,
        "video_url": first_part.video_url,
        "course_text": first_part.description
    }

    self_support_course_schema = SelfSupportCourse(**self_support_course)

    return self_support_course_schema


@app.post("/register")
async def register(registration_data: RegistrationData, db: Session = Depends(get_db)) -> RegistrationResponse:
    """Register a new user"""
    try:
        return await registration(registration_data, db)
    except RegistrationException as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {e}")


@app.get("/is-registered/{sm_id}")
async def is_registered(sm_id: str, db: Session = Depends(get_db)) -> dict:
    """Check if a user is registered by email"""
    user = db.query(User).filter(
        (User.telegram_id == sm_id) | (User.vk_id == sm_id)
    ).first()

    if user:
        return {"is_registered": True, "message": "User is registered"}
    else:
        return {"is_registered": False, "message": "User is not registered"}


@app.get("/random-history/{sm_id}")
async def get_random_history(sm_id: str, db: Session = Depends(get_db)):
    """Get a random unseen story for a user"""

    user = db.query(User).filter(
        (User.telegram_id == sm_id) | (User.vk_id == sm_id)
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    viewed_story_ids = db.query(StoryHistory.story_id).filter(
        StoryHistory.user_id == user.id
    ).all()
    viewed_story_ids = [story_id[0] for story_id in viewed_story_ids]

    unseen_stories = db.query(Story).filter(
        ~Story.id.in_(viewed_story_ids) & (Story.is_agreed_to_publication)
    ).all()

    if not unseen_stories:
        return {"success": False, "message": "К сожалению, нет новых историй"}

    random_story: Story = random.choice(unseen_stories)

    if random_story.is_anonymous:
        history_author = "Анонимный автор"
    else:
        if random_story.user_id:
            history_author = f"{random_story.user.first_name} {random_story.user.last_name}"
        else:
            history_author = random_story.user_name

    is_anonymous = random_story.is_anonymous \
        if random_story.is_anonymous is not None else False
    is_agreed_to_publication = random_story.is_agreed_to_publication \
        if random_story.is_agreed_to_publication is not None else False

    history_data = {
        "author": history_author if history_author else None,
        "title": random_story.title if random_story.title else None,
        "text": random_story.text if random_story.text else None,
        "media_url": random_story.media_url or None,
        "link": random_story.link or None,
        "is_anonymous": is_anonymous,
        "is_agreed_to_publication": is_agreed_to_publication,
        "content_type": random_story.content_type,
    }
    history_data = HistoryData(**history_data)

    history_response = HistoryResponse(
        success=True,
        message="История успешно получена",
        history=history_data
    )

    story_history = StoryHistory(story_id=random_story.id, user_id=user.id)
    db.add(story_history)
    db.commit()

    return history_response


@app.post("/send-feedback")
async def send_feedback(feedback: Feedback, db: Session = Depends(get_db)) -> Feedback:
    """Send feedback to the museum"""

    # TODO: Save feedback to database
    return feedback
