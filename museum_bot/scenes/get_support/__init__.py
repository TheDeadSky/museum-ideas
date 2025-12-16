from aiogram import Router, F

from .get_support_scene import GetSupportScene
from .self_support_course_scene import SelfSupportCourseScene
from .show_colleagues_stories import ShowColleaguesStoriesScene

get_support_router = Router()

get_support_router.callback_query.register(GetSupportScene.as_handler(), F.data == "get_support")
get_support_router.message.register(GetSupportScene.as_handler(), F.text.casefold() == "получить поддержку")
get_support_router.callback_query.register(SelfSupportCourseScene.as_handler(), F.data == "self_support_course")

get_support_scenes_registry = (
    GetSupportScene,
    SelfSupportCourseScene,
    ShowColleaguesStoriesScene
)

__all__ = [
    "get_support_router",
    "get_support_scenes_registry",
]
