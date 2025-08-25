from vkbottle.bot import Message, BotLabeler

from menus import CONFIRMATION_MENU, TO_MAIN_MENU_BUTTON
from services.api_service import send_feedback, get_text_from_db
from models.feedback import Feedback
from utils import make_one_button_menu
from states.general_states import GeneralStates

feedback_labeler = BotLabeler()


@feedback_labeler.message(text="Обратная связь")
@feedback_labeler.message(text="отзыв")
@feedback_labeler.message(payload="feedback", state=GeneralStates.MAIN_MENU)
async def on_feedback_handler(self, message: Message):
    feedback_entry_message = await get_text_from_db("feedback_entry_message")

    await message.answer(
        feedback_entry_message,
        reply_markup=make_one_button_menu("Отмена", "menu")
    )


@feedback_labeler.message(state=GeneralStates.FEEDBACK)
async def handle_feedback(self, message: Message):
    data = {}
    data["feedback_text"] = message.text

    await message.answer(
        "Подтвердите отправку сообщения:",
        reply_markup=CONFIRMATION_MENU
    )


@feedback_labeler.message(payload="confirm", state=GeneralStates.FEEDBACK)
async def confirm_feedback(self, message: Message):
    data = {}

    await send_feedback(
        Feedback(
            sm_id=str(message.peer_id),
            feedback=data["feedback_text"]
        )
    )

    feedback_accepted_message = await get_text_from_db("feedback_accepted_message")

    await message.answer(feedback_accepted_message, reply_markup=TO_MAIN_MENU_BUTTON)


@feedback_labeler.message(payload="not_confirm", state=GeneralStates.FEEDBACK)
async def not_confirm_feedback(self, message: Message):
    await message.answer("Отправка отменена")
