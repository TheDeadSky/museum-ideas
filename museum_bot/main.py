import asyncio
import logging
from os import getenv

from aiogram.fsm.scene import SceneRegistry
from aiogram.fsm.storage.memory import SimpleEventIsolation

from handlers.commands.main_commands import mc_router

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from scenes.registration import registration_scenes_router, registration_scenes_registry
from scenes.main_menu import main_menu_router, main_menu_scenes_registry
from scenes.get_support import get_support_router, get_support_scenes_registry
from scenes.share_experience import share_experience_router, share_experience_scenes_registry

TOKEN = getenv("BOT_TOKEN")


async def main() -> None:
    dispatcher = Dispatcher(
        events_isolation=SimpleEventIsolation(),
    )

    scenes_registry = SceneRegistry(dispatcher)

    scenes_registry.add(
        *registration_scenes_registry,
        *main_menu_scenes_registry,
        *get_support_scenes_registry,
        *share_experience_scenes_registry,
    )

    dispatcher.include_routers(
        mc_router,
        registration_scenes_router,
        main_menu_router,
        get_support_router,
        share_experience_router,
    )

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
