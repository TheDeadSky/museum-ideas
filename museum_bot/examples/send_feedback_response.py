"""
Example script demonstrating how to send feedback responses to users
via the bot's external API endpoints.
"""

import asyncio
import aiohttp
import json
from typing import Optional


async def send_feedback_response(
    user_id: str,
    response_text: str,
    feedback_id: Optional[str] = None,
    bot_api_url: str = "http://localhost:3000"
) -> dict:
    """
    Send a feedback response to a user via the bot's external API.

    Args:
        user_id: Telegram user ID to send the response to
        response_text: The response text to send
        feedback_id: Optional feedback ID for reference
        bot_api_url: Base URL of the bot's API server

    Returns:
        API response as dictionary
    """
    payload = {
        "user_id": user_id,
        "response_text": response_text,
        "feedback_id": feedback_id
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{bot_api_url}/api/send-feedback-response",
            json=payload
        ) as response:
            return await response.json()


async def send_generic_message(
    user_id: str,
    message: str,
    bot_api_url: str = "http://localhost:3000"
) -> dict:
    """
    Send a generic message to a user via the bot's external API.

    Args:
        user_id: Telegram user ID to send the message to
        message: The message text to send
        bot_api_url: Base URL of the bot's API server

    Returns:
        API response as dictionary
    """
    payload = {
        "user_id": user_id,
        "message": message
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{bot_api_url}/api/send-message",
            json=payload
        ) as response:
            return await response.json()


async def main():
    """Example usage of the external API endpoints"""

    # Example user ID (replace with actual user ID)
    example_user_id = "123456789"

    print("=== Feedback Response Example ===")

    # Send a feedback response
    try:
        response = await send_feedback_response(
            user_id=example_user_id,
            response_text="Thank you for your feedback! We appreciate your input and will take it into consideration.",
            feedback_id="fb_12345"
        )
        print(f"Feedback response result: {json.dumps(response, indent=2)}")
    except Exception as e:
        print(f"Error sending feedback response: {e}")

    print("\n=== Generic Message Example ===")

    # Send a generic message
    try:
        response = await send_generic_message(
            user_id=example_user_id,
            message="Hello! This is a test message from the external API."
        )
        print(f"Generic message result: {json.dumps(response, indent=2)}")
    except Exception as e:
        print(f"Error sending generic message: {e}")


if __name__ == "__main__":
    asyncio.run(main())
