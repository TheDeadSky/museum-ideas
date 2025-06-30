from sqlalchemy.orm import Session

from db.models import Story
from db.utils import get_user_by_sm_id
from schemas import BaseResponse
from .schemas import ShareExperienceData
from .enums import ExperienceStatus


async def save_user_experience(data: ShareExperienceData, db: Session) -> BaseResponse:
    user = get_user_by_sm_id(db, data.sm_id)

    user_name = user.firstname
    if user.lastname:
        user_name += " " + user.lastname

    story = Story(
        user_id=user.id,
        user_name=user_name,
        status=ExperienceStatus.MODERATION,
        text=data.experience,
        is_anonymous=data.is_anonymous,
        is_agreed_to_publication=data.publish
    )

    db.add(story)
    db.commit()

    return BaseResponse(
        success=True,
        message="Спасибо, что поделились опытом. Ваша история отправлена на модерацию."
    )
