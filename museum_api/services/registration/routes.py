from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from .actions import registration, RegistrationException, is_user_registered
from .schemas import RegistrationData, RegistrationResponse

router = APIRouter()


@router.post("/register")
async def register(registration_data: RegistrationData, db: Session = Depends(get_db)) -> RegistrationResponse:
    """Register a new user"""
    try:
        return await registration(registration_data, db)
    except RegistrationException as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {e}")


@router.get("/is-registered/{sm_id}")
async def is_registered(sm_id: str, db: Session = Depends(get_db)) -> RegistrationResponse:
    """Check if a user is registered by email"""
    return await is_user_registered(sm_id, db)
