from vkbottle.bot import BotLabeler, Message

from menus import ONE_MORE_STORY_BUTTON, TO_MAIN_MENU_BUTTON
from services.api_service import get_random_history
from utils import fetch_audio_binary, make_one_button_menu, merge_inline_menus
from states.general_states import GeneralStates
from settings import voice_uploader


colleagues_stories_labeler = BotLabeler()


@colleagues_stories_labeler.message(payload="colleagues_stories", state=GeneralStates.GET_SUPPORT)
async def on_enter_show_colleagues_stories(message: Message):
    history_response = await get_random_history(
        str(message.peer_id)
    )

    if not history_response.success:
        await message.answer(
            text=history_response.message,
            keyboard=merge_inline_menus(
                make_one_button_menu("Добавить историю", "share_experience"),
                TO_MAIN_MENU_BUTTON
            )
        )
        return

    story = history_response.history

    display_text = ""

    if story.author and not story.is_anonymous:
        display_text += f"{story.author}\n\n"

    if story.title:
        display_text += f"{story.title}\n\n"

    if story.text:
        if display_text:
            display_text += "\n"
        display_text += story.text

    if story.content_type == "text":
        await message.answer(
            display_text,
            keyboard=merge_inline_menus(
                ONE_MORE_STORY_BUTTON,
                TO_MAIN_MENU_BUTTON
            )
        )

    elif story.content_type == "audio":
        await message.answer(
            "Временно недоступно",
            keyboard=merge_inline_menus(
                ONE_MORE_STORY_BUTTON,
                TO_MAIN_MENU_BUTTON
            )
        )
        # await message.answer(
        #     display_text
        # )

        audio_binary = await fetch_audio_binary(story.media_url)
        buffered_audio = await voice_uploader.upload(
            audio_binary,
            title=f"story_voice_{message.peer_id}.ogg"
        )

        await message.answer(
            attachment=buffered_audio,
            reply_markup=merge_inline_menus(
                ONE_MORE_STORY_BUTTON,
                TO_MAIN_MENU_BUTTON
            )
        )


@colleagues_stories_labeler.message(payload="one_more_story", state=GeneralStates.GET_SUPPORT)
async def on_one_more_story(message: Message):
    await on_enter_show_colleagues_stories(message)
