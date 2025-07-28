from sqlalchemy.orm import Session
from db.models import Story, StoryHistory
from services.share_experience.enums import ExperienceStatus


def get_viewed_story_ids(db: Session, user_id: int) -> list[int]:
    """Get list of story IDs that user has already viewed"""
    viewed_story_ids = db.query(StoryHistory.story_id).filter(
        StoryHistory.user_id == user_id
    ).all()
    return [story_id[0] for story_id in viewed_story_ids]


def get_unseen_stories(db: Session, viewed_story_ids: list[int]) -> list[Story]:
    """Get stories that user hasn't viewed yet and are agreed to publication"""
    return db.query(Story).filter(
        ~Story.id.in_(viewed_story_ids)
        & (Story.is_agreed_to_publication)
        & (Story.status == ExperienceStatus.ACCEPTED)
    ).all()


def get_history_author(story: Story) -> str:
    """Get the author name for a story"""
    if story.is_anonymous:
        return "Анонимный автор"

    if story.user_id and story.user:
        if story.user.firstname and story.user.lastname:
            return f"{story.user.firstname} {story.user.lastname}"
        elif story.user.firstname:
            return story.user.firstname
        return story.user_name

    return story.user_name or "Неизвестный автор"
