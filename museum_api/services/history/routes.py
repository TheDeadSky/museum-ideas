from fastapi import Depends, HTTPException
from fastapi import APIRouter
from sqlalchemy.orm import Session

from db.database import get_db
from .actions import get_random_history
from .exceptions import HistoryException


router = APIRouter()


@router.get("/random-history/{sm_id}")
async def get_random_history_endpoint(sm_id: str, db: Session = Depends(get_db)):
    """Get a random unseen story for a user"""
    try:
        return await get_random_history(sm_id, db)
    except HistoryException as e:
        raise HTTPException(status_code=404, detail=str(e))
