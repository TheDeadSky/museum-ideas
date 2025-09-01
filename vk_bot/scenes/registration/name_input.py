from vkbottle.bot import Message, BotLabeler, rules, MessageEvent
from vkbottle_types.events.bot_events import GroupEventType

from states.registration import Registration
from services.api_service import get_text_from_db
from settings import state_dispenser
from actions.general import make_confirmation_menu, make_yes_no_menu


def init(labeler: BotLabeler):
    @labeler.message(state=Registration.REGISTRATION_NAME)
    async def name_input_handler(message: Message):
        await state_dispenser.set(
            message.peer_id,
            Registration.REGISTRATION_NAME_CONFIRMATION,
            firstname=message.text
        )
        name_confirmation_message = await get_text_from_db("name_confirmation_message")
        confirmation_menu = make_confirmation_menu(for_state=Registration.REGISTRATION_NAME_CONFIRMATION.value)
        await message.answer(
            name_confirmation_message.format(message.text),
            keyboard=confirmation_menu
        )

    @labeler.raw_event(
        GroupEventType.MESSAGE_EVENT,
        MessageEvent,
        rules.PayloadRule({
            "cmd": "not_confirm",
            "state": Registration.REGISTRATION_NAME_CONFIRMATION.value
        })
    )
    async def not_confirm(event: MessageEvent):
        state_peer = await state_dispenser.get(event.peer_id)

        if state_peer is None:
            state_payload = {}
        else:
            state_payload = state_peer.payload

        state_payload.update({
            "firstname": None
        })
        await state_dispenser.set(
            event.peer_id,
            Registration.REGISTRATION_NAME,
            **state_payload
        )
        await event.send_message("Введите Ваше имя заново.")

    @labeler.raw_event(
        GroupEventType.MESSAGE_EVENT,
        MessageEvent,
        rules.PayloadRule({
            "cmd": "confirm",
            "state": Registration.REGISTRATION_NAME_CONFIRMATION.value
        })
    )
    async def confirm(event: MessageEvent):
        await state_dispenser.set(
            event.peer_id,
            Registration.REGISTRATION_IS_MUSEUM_WORKER
        )
        is_museum_worker_question = await get_text_from_db("is_museum_worker_question")
        await event.send_message(
            is_museum_worker_question,
            keyboard=make_yes_no_menu(for_state=Registration.REGISTRATION_IS_MUSEUM_WORKER.value)
        )
