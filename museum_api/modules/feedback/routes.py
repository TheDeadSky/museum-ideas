import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from db.database import get_db
from schemas import BaseResponse
from .actions import render_feedbacks_page, save_user_feedback, get_feedbacks, answer_feedback
from .schemas import FeedbackListResponse, FeedbackAnswerData, IncomingFeedback

router = APIRouter()


@router.post("/send-feedback")
async def send_feedback(feedback: IncomingFeedback, db: Session = Depends(get_db)) -> BaseResponse:
    """Send feedback to the museum"""

    return await save_user_feedback(feedback, db)


@router.get("/admin/feedbacks", response_class=HTMLResponse)
async def feedbacks_page(key: str = Query(default="")):
    """Get feedbacks page"""

    logging.info(key)

    if key == "sHHUc6u3VTgP*WSu1vz^p@8zC!Y":
        return await render_feedbacks_page()

    raise HTTPException(status_code=404, detail="Not found")


@router.get("/feedback/list")
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


@router.post("/feedback/answer")
async def answer_feedback_endpoint(answer_data: FeedbackAnswerData, db: Session = Depends(get_db)) -> BaseResponse:
    """Answer feedback"""

    return await answer_feedback(answer_data, db)
