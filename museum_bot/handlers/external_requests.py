import logging
from aiohttp import web
from aiogram import Bot

from models.feedback import FeedbackAnswer

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

            # Send message to user
            await self.bot.send_message(
                chat_id=feedback_request.user_id,
                text=feedback_request.response_text
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
            user_id = data.get("user_id")
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


def setup_external_routes(app: web.Application, bot: Bot) -> None:
    """Setup external request routes"""
    handler = ExternalRequestHandler(bot)

    # Add routes for external requests
    app.router.add_post("/api/send-feedback-response", handler.send_feedback_response)
    app.router.add_post("/api/send-message", handler.send_message_to_user)
