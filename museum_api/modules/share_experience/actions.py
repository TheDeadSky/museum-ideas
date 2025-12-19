from sqlalchemy.orm import Session

from db.models import Story
from db.utils import define_user_platform, get_user_by_sm_id
from shared.models import BaseResponse
from .models import ShareExperienceData
from .enums import ExperienceStatus, ContentType


async def save_user_experience(data: ShareExperienceData, db: Session) -> BaseResponse:
    user = get_user_by_sm_id(db, data.sm_id)

    if not user:
        return BaseResponse(
            success=False,
            message=f"User not found by sm_id: {data.sm_id}."
        )

    user_name = user.firstname
    if user_name and user.lastname:
        user_name += " " + user.lastname

    platform = define_user_platform(db, user)

    if user_name is None:
        if platform == "tg" and user.tg_username:
            user_name = user.tg_username
        else:
            user_name = f"Unknown_{platform}_{data.sm_id}"

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
