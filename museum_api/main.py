import json
from typing import Annotated, List
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, Response, Depends
from sqlalchemy.orm import Session

from utils import escape_tg_reserved_characters
from schemas import Feedback, SelfSupportCourse, SelfSupportCourseBeginnerData
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

    return {key: escape_tg_reserved_characters(bot_texts[key]) for key in keys}


@app.post("/begin-self-support-course")
async def begin_self_support_course(beginner_data: SelfSupportCourseBeginnerData) -> SelfSupportCourse:
    with open("db_imitation/self_support_course.json", "r", encoding="utf-8") as f:
        self_support_course = json.load(f)

    self_support_course_schema = SelfSupportCourse(**self_support_course)

    return self_support_course_schema


@app.post("/send-feedback")
async def send_feedback(feedback: Feedback, db: Session = Depends(get_db)) -> Feedback:
    # TODO: Save feedback to database
    return feedback


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
