from fastapi import Depends
from fastapi import APIRouter
from sqlalchemy.orm import Session

from db.database import get_db
from modules.common.actions import send_message_for_all
from modules.common.models import MessageForAll

router = APIRouter()


@router.post("/message-for-all")
async def send_message_to_all_users(message_for_all: MessageForAll, db: Session = Depends(get_db)):
    await send_message_for_all(message_for_all, db)
