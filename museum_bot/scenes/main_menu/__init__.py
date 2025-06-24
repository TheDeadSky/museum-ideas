from aiogram import Router, F

from .main_menu_scene import MainMenuScene
from .about_project_scene import AboutProjectScene
from .feedback_scene import FeedbackScene

main_menu_router = Router()

main_menu_router.callback_query.register(MainMenuScene.as_handler(), F.data == "menu")
main_menu_router.message.register(MainMenuScene.as_handler(), F.text.casefold() == "меню")

main_menu_scenes_registry = (
    MainMenuScene,
    AboutProjectScene,
    FeedbackScene,
)

__all__ = [
    "main_menu_router",
    "main_menu_scenes_registry",
]
