import asyncio

from fastapi import APIRouter, Depends
from vkbottle import Bot

from bot import get_vk_bot
from menus import TO_MAIN_MENU_BUTTON
from models import BaseResponse
from models.base import SendMessageToAllRequest
from models.course import CourseNotificationData
from models.feedback import FeedbackAnswer
from utils import merge_inline_menus, make_one_button_menu

vk_bot_actions_router = APIRouter()


@vk_bot_actions_router.post("/vk-bot/send-feedback-answer")
async def send_feedback_answer(feedback_answer: FeedbackAnswer, bot: Bot = Depends(get_vk_bot)):
    answer_text = (
        f"Ваш текст:\n{feedback_answer.feedback_text}\n\n"
        f"Ответ:\n{feedback_answer.answer_text}"
    )

    await bot.api.messages.send(
        peer_id=int(feedback_answer.sm_id),
        message=answer_text
    )

    return BaseResponse(success=True, message="Feedback answer sent successfully")


@vk_bot_actions_router.post("/vk-bot/new-chapter-notification")
async def notify_users_about_course(notification: CourseNotificationData, bot: Bot = Depends(get_vk_bot)):
    queue = 10

    menu = merge_inline_menus(
        make_one_button_menu("Перейти к курсу", {"cmd": "self_support_course"}),
        TO_MAIN_MENU_BUTTON
    )

    for user_id in notification.users_with_progress:
        await bot.api.messages.send(
            peer_id=int(user_id),
            message="Появилась новая часть курса!",
            keyboard=menu.get_json()
        )

        queue -= 1
        if queue == 0:
            await asyncio.sleep(2)
            queue = 10

    for user_id in notification.users_without_progress:
        await bot.api.messages.send(
            peer_id=int(user_id),
            message=(
                "Сегодня вышла новая лекция курса. "
                "Вы получите к ней доступ по ссылке ниже, если ответили на вопросы прошлых лекций."
            ),
            keyboard=menu.get_json()
        )

        queue -= 1
        if queue == 0:
            await asyncio.sleep(2)
            queue = 10

    return BaseResponse(success=True, message="Users notified successfully")


@vk_bot_actions_router.post("/vk-bot/send-message-to-all")
async def send_message_to_all(message_data: SendMessageToAllRequest, bot: Bot = Depends(get_vk_bot)):
    queue = 10

    menu = TO_MAIN_MENU_BUTTON

    for user_id in message_data.sm_ids:
        await bot.api.messages.send(
            peer_id=int(user_id),
            message=message_data.message,
            keyboard=menu.get_json()
        )

        queue -= 1
        if queue == 0:
            await asyncio.sleep(2)
            queue = 10

    return BaseResponse(success=True, message="Users notified successfully")
