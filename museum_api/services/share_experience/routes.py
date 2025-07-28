from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from .actions import save_user_experience
from .schemas import ShareExperienceData
from schemas import BaseResponse

router = APIRouter()


@router.post("/share-experience")
async def share_experience(data: ShareExperienceData, db: Session = Depends(get_db)) -> BaseResponse:
    return await save_user_experience(data, db)
