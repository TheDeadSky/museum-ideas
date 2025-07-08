import logging
import asyncio
from aiohttp import web
from aiogram import Bot

from menus import TO_MAIN_MENU_BUTTON
from models.feedback import FeedbackAnswer
from models.course import CourseNotificationData
from utils import make_one_button_menu, merge_inline_menus

logger = logging.getLogger(__name__)


class ExternalRequestHandler:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def send_feedback_response(self, request: web.Request) -> web.Response:
        """Handle external request to send feedback response to user"""
        try:
            # Parse request body
            data = await request.json()
            feedback_request = FeedbackAnswer(**data)

            answer_text = f"<blockquote>{feedback_request.feedback_text}</blockquote>\n\n{feedback_request.answer_text}"

            # Send message to user
            await self.bot.send_message(
                chat_id=feedback_request.sm_id,
                text=answer_text
            )

            logger.info(f"Feedback response sent to user {feedback_request.user_id}")

            return web.json_response({
                "success": True,
                "message": "Feedback response sent successfully",
                "user_id": feedback_request.user_id,
                "feedback_id": feedback_request.feedback_id
            })

        except Exception as e:
            logger.error(f"Error sending feedback response: {str(e)}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=500)

    async def send_message_to_user(self, request: web.Request) -> web.Response:
        """Generic endpoint to send any message to a user"""
        try:
            data = await request.json()
            user_id = data.get("sm_id")
            message_text = data.get("message")

            if not user_id or not message_text:
                return web.json_response({
                    "success": False,
                    "error": "user_id and message are required"
                }, status=400)

            # Send message to user
            await self.bot.send_message(
                chat_id=user_id,
                text=message_text
            )

            logger.info(f"Message sent to user {user_id}")

            return web.json_response({
                "success": True,
                "message": "Message sent successfully",
                "user_id": user_id
            })

        except Exception as e:
            logger.error(f"Error sending message to user: {str(e)}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=500)

    async def notify_users_about_course(self, request: web.Request) -> web.Response:
        """Notify users about course"""

        raw_data = await request.json()

        data = CourseNotificationData(**raw_data)

        queue = 10

        for user_id in data.users_with_progress:
            await self.bot.send_message(
                chat_id=user_id,
                text="Появилась новая часть курса!",
                reply_markup=merge_inline_menus(
                    make_one_button_menu("Перейти к курсу", "self_support_course"),
                    TO_MAIN_MENU_BUTTON
                )
            )
            queue -= 1
            if queue == 0:
                await asyncio.sleep(2)
                queue = 10

        for user_id in data.users_without_progress:
            await self.bot.send_message(
                chat_id=user_id,
                text="Появилась новая часть курса! Пройдите курс самоподдержки, чтобы не пропустить новые уроки!",
                reply_markup=merge_inline_menus(
                    make_one_button_menu("Перейти к курсу", "self_support_course"),
                    TO_MAIN_MENU_BUTTON
                )
            )

            queue -= 1
            if queue == 0:
                await asyncio.sleep(2)

        return web.json_response({
            "success": True,
            "message": "Users notified successfully"
        })


def setup_external_routes(app: web.Application, bot: Bot) -> None:
    """Setup external request routes"""
    handler = ExternalRequestHandler(bot)

    # Add routes for external requests
    app.router.add_post("/api/send-feedback-answer", handler.send_feedback_response)
    app.router.add_post("/api/send-message", handler.send_message_to_user)
    app.router.add_post("/api/notify-users-about-course", handler.notify_users_about_course)
