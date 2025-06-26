import random
from sqlalchemy.orm import Session
from db.models import Story, StoryHistory
from schemas import HistoryData, HistoryResponse
from services.history.exceptions import HistoryException
from services.history.utils import (
    get_viewed_story_ids,
    get_unseen_stories,
    get_history_author
)
from db.utils import get_user_by_sm_id


async def get_random_history(sm_id: str, db: Session) -> HistoryResponse:
    """Get a random unseen story for a user"""

    user = get_user_by_sm_id(db, sm_id)
    if not user:
        raise HistoryException("User not found")

    viewed_story_ids = get_viewed_story_ids(db, user.id)

    unseen_stories = get_unseen_stories(db, viewed_story_ids)

    if not unseen_stories:
        return HistoryResponse(
            success=False,
            message="К сожалению, нет новых историй"
        )

    random_story: Story = random.choice(unseen_stories)

    history_author = get_history_author(random_story)

    is_anonymous = (
        random_story.is_anonymous
        if random_story.is_anonymous is not None
        else False
    )
    is_agreed_to_publication = (
        random_story.is_agreed_to_publication
        if random_story.is_agreed_to_publication is not None
        else False
    )

    history_data = HistoryData(
        author=history_author if history_author else None,
        title=random_story.title if random_story.title else None,
        text=random_story.text if random_story.text else None,
        media_url=random_story.media_url or None,
        link=random_story.link or None,
        is_anonymous=is_anonymous,
        is_agreed_to_publication=is_agreed_to_publication,
        content_type=random_story.content_type,
    )

    history_response = HistoryResponse(
        success=True,
        message="История успешно получена",
        history=history_data
    )

    story_history = StoryHistory(story_id=random_story.id, user_id=user.id)
    db.add(story_history)
    db.commit()

    return history_response
