from vkbottle.bot import Message, BotLabeler, rules, MessageEvent
from vkbottle_types.events.bot_events import GroupEventType

from actions.general import make_confirmation_menu
from menus import TO_MAIN_MENU_BUTTON
from services.api_service import send_feedback, get_text_from_db
from utils import make_one_button_menu, get_state_payload
from states.feedback import FeedbackStates
from models.feedback import Feedback
from settings import state_dispenser

feedback_labeler = BotLabeler()


@feedback_labeler.message(text="Обратная связь")
@feedback_labeler.message(text="отзыв")
async def on_feedback_message_handler(message: Message):
    feedback_entry_message = await get_text_from_db("feedback_entry_message")

    await state_dispenser.set(
        message.peer_id,
        FeedbackStates.INPUT
    )

    await message.answer(
        feedback_entry_message,
        keyboard=make_one_button_menu("Отмена", {"cmd": "main_menu"}).get_json()
    )


@feedback_labeler.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadRule({"cmd": "feedback"})
)
async def on_feedback_event_handler(event: MessageEvent):
    feedback_entry_message = await get_text_from_db("feedback_entry_message")

    await state_dispenser.set(
        event.peer_id,
        FeedbackStates.INPUT
    )

    await event.send_message(
        feedback_entry_message,
        keyboard=make_one_button_menu("Отмена", {"cmd": "main_menu"}, "callback").get_json()
    )


@feedback_labeler.message(state=FeedbackStates.INPUT)
async def handle_feedback(message: Message):
    data = {}
    data["feedback_text"] = message.text

    await state_dispenser.set(
        message.peer_id,
        FeedbackStates.CONFIRM,
        **data
    )

    await message.answer(
        "Подтвердите отправку сообщения:",
        keyboard=make_confirmation_menu(for_state=FeedbackStates.CONFIRM.value)
    )


@feedback_labeler.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadRule({"cmd": "confirm", "state": FeedbackStates.CONFIRM.value})
)
async def confirm_feedback(event: MessageEvent):
    data = await get_state_payload(state_dispenser, event.peer_id)

    await send_feedback(
        Feedback(
            sm_id=str(event.peer_id),
            feedback=data["feedback_text"]
        )
    )

    feedback_accepted_message = await get_text_from_db("feedback_accepted_message")

    await event.send_message(feedback_accepted_message, keyboard=TO_MAIN_MENU_BUTTON.get_json())


@feedback_labeler.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadRule({"cmd": "not_confirm", "state": FeedbackStates.CONFIRM.value})
)
async def not_confirm_feedback(event: MessageEvent):
    await event.send_message("Отправка отменена", keyboard=TO_MAIN_MENU_BUTTON.get_json())
