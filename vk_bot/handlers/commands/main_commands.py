from vkbottle.bot import BotLabeler, Message
from actions.main_menu import default_main_menu
from actions.registration import make_registration_button
from services.api_service import get_is_registered, get_text_from_db
from menus import MAIN_MENU
from states.registration import Registration
from settings import state_dispenser, video_uploader

commands_labeler = BotLabeler()


# @commands_labeler.message(command="/start")
@commands_labeler.message(text="Начать")
async def start_handler(message: Message):
    vk_id = str(message.from_id)

    is_registered_response = await get_is_registered(vk_id)
    if is_registered_response["success"]:
        main_menu_text = await get_text_from_db("main_menu_text")
        await default_main_menu(
            message,
            main_menu_text
        )
        return

    await state_dispenser.set(
        message.peer_id,
        Registration.REGISTRATION_START
    )

    greetings = await get_text_from_db("start_greetings")

    await message.answer(greetings, keyboard=make_registration_button().get_json())


@commands_labeler.message(command="/dev_menu")
async def menu_handler(message: Message):
    await message.answer("Главное меню:", keyboard=MAIN_MENU.get_json())


@commands_labeler.message(command="test_vid")
async def test_vid_handler(message: Message):
    # video = await video_uploader.upload(
    #     file_source="https://ideasformuseums.com/botimages/video/course-1_lecture-1.mp4",
    #     peer_id=message.peer_id,
    #     owner_id=-229734251
    # )
    await message.answer("🎥 Видео:")
    await message.answer(attachment="clip-229734251_456239028")
