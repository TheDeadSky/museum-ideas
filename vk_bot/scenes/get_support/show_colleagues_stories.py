from vkbottle.bot import BotLabeler, rules, MessageEvent
from vkbottle_types.events.bot_events import GroupEventType


from menus import ONE_MORE_STORY_BUTTON, TO_MAIN_MENU_BUTTON
from services.api_service import get_random_history
from utils import fetch_binary_data, make_one_button_menu, merge_inline_menus
from settings import voice_uploader


colleagues_stories_labeler = BotLabeler()


@colleagues_stories_labeler.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadRule({
        "cmd": "colleagues_stories"
    })
)
async def on_enter_show_colleagues_stories(event: MessageEvent):
    history_response = await get_random_history(
        str(event.peer_id)
    )

    if not history_response.success or not history_response.history:
        await event.send_message(
            history_response.message,
            keyboard=merge_inline_menus(
                make_one_button_menu("Добавить историю", {"cmd": "share_experience"}),
                TO_MAIN_MENU_BUTTON
            ).get_json()
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
        await event.send_message(
            display_text,
            keyboard=merge_inline_menus(
                ONE_MORE_STORY_BUTTON,
                TO_MAIN_MENU_BUTTON
            ).get_json()
        )

    elif story.content_type == "audio":
        await event.send_message(
            "Временно недоступно",
            keyboard=merge_inline_menus(
                ONE_MORE_STORY_BUTTON,
                TO_MAIN_MENU_BUTTON
            ).get_json()
        )
        # await message.answer(
        #     display_text
        # )

        audio_binary = await fetch_binary_data(story.media_url)
        buffered_audio = await voice_uploader.upload(
            audio_binary,
            title=f"story_voice_{event.peer_id}.ogg"
        )

        await event.send_message(
            attachment=buffered_audio,
            keyboard=merge_inline_menus(
                ONE_MORE_STORY_BUTTON,
                TO_MAIN_MENU_BUTTON
            ).get_json()
        )


@colleagues_stories_labeler.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadRule({
        "cmd": "one_more_story"
    })
)
async def on_one_more_story(event: MessageEvent):
    await on_enter_show_colleagues_stories(event)
