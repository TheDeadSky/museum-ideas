from sqlalchemy.orm import Session

from db.models import Story
from db.utils import get_user_by_sm_id
from schemas import BaseResponse
from .schemas import ShareExperienceData
from .enums import ExperienceStatus, ContentType


async def save_user_experience(data: ShareExperienceData, db: Session) -> BaseResponse:
    user = get_user_by_sm_id(db, data.sm_id)

    user_name = user.firstname
    if user.lastname:
        user_name += " " + user.lastname

    content_type = ContentType.TEXT
    if data.experience_type == "audio":
        content_type = ContentType.AUDIO

    story = Story(
        user_id=user.id,
        user_name=user_name,
        status=ExperienceStatus.MODERATION,
        content_type=content_type,
        is_anonymous=data.is_anonymous,
        is_agreed_to_publication=data.publish
    )

    if content_type == ContentType.TEXT:
        story.text = data.experience
    else:
        story.media_url = data.experience

    db.add(story)
    db.commit()

    return BaseResponse(
        success=True,
        message="Спасибо, что поделились опытом. Ваша история отправлена на модерацию."
    )
