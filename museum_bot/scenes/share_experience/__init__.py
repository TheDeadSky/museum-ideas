from aiogram import F, Router

from .share_experience_scene import ShareExperienceScene
from .confirmation_scene import ConfirmationScene
from .publication_scene import PublicationScene
from .anonymity_scene import AnonymityScene
from .submit_share_experience import SubmitShareExperienceScene

share_experience_router = Router()

share_experience_router.callback_query.register(ShareExperienceScene.as_handler(), F.data == "share_experience")
share_experience_router.message.register(ShareExperienceScene.as_handler(), F.text.casefold() == "поделиться опытом")

share_experience_scenes_registry = (
    ShareExperienceScene,
    ConfirmationScene,
    PublicationScene,
    AnonymityScene,
    SubmitShareExperienceScene,
)

__all__ = [
    "share_experience_router",
    "share_experience_scenes_registry",
]
