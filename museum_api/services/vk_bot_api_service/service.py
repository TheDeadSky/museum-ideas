import aiohttp
from typing import Optional

from config import settings
from shared.models import (
    SendFeedbackAnswerRequest,
    SendMessageToAllRequest,
    NotifyUsersAboutCourseRequest,
    ApiResponse
)


class VkBotAPIService:
    """
    Service for sending requests to the VK bot API
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
    ):
        """
        Initialize the API service with base URL

        Args:
            base_url: Base URL for the VK bot API (defaults to config setting)
        """
        self.base_url = (base_url or settings.VK_BOT_API_BASE_URL).rstrip('/')

    async def send_feedback_answer(
        self,
        sm_id: str,
        answer_text: str,
        feedback_text: str
    ) -> ApiResponse:
        """
        Send feedback answer to user

        Args:
            sm_id: Social media ID of the user
            answer_text: Answer text to send
            feedback_text: Original feedback text

        Returns:
            ApiResponse: API response
        """
        request_data = SendFeedbackAnswerRequest(
            sm_id=sm_id,
            answer_text=answer_text,
            feedback_text=feedback_text
        )

        url = f"{self.base_url}/vk-bot/send-feedback-answer"

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=request_data.model_dump()) as response:
                response_json = await response.json()
                return ApiResponse(**response_json)

    async def send_message_to_all(
        self,
        message: str,
        vk_ids: list[str]
    ) -> ApiResponse:
        """
        Send message to all users

        Args:
            message: Message to send
            vk_ids: List of VK IDs (if None, sends to all)

        Returns:
            ApiResponse: API response
        """
        request_data = SendMessageToAllRequest(
            message=message,
            sm_ids=vk_ids
        )

        url = f"{self.base_url}/vk-bot/send-message-to-all"

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=request_data.model_dump()) as response:
                response_json = await response.json()
                return ApiResponse(**response_json)

    async def notify_users_about_course(
        self,
        users_with_progress: list[str],
        users_without_progress: list[str]
    ) -> ApiResponse:
        """
        Notify users about course

        Args:
            users_with_progress: List of user IDs with progress
            users_without_progress: List of user IDs without progress

        Returns:
            ApiResponse: API response
        """
        request_data = NotifyUsersAboutCourseRequest(
            users_with_progress=users_with_progress,
            users_without_progress=users_without_progress
        )

        url = f"{self.base_url}/vk-bot/notify-users-about-course"

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=request_data.model_dump()) as response:
                response_json = await response.json()
                return ApiResponse(**response_json)
