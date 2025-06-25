import json
import os
import aiohttp

from models.registration import RegistrationData
from models.stories import HistoryResponse


async def get_self_support_course():
    # async with aiohttp.ClientSession() as session:
    #     async with session.get("https://api.example.com/self-support-course") as response:
    #         return await response.json()

    with open("src/self_support_course.json", "r", encoding="utf-8") as file:
        return json.load(file)


async def get_text_from_db(text_key: str):
    with open("src/texts_in_db.json", "r", encoding="utf-8") as file:
        return json.load(file)[text_key]


async def get_achievement_photo_url():
    with open("src/achievement_photo_url.json", "r", encoding="utf-8") as file:
        return json.load(file)["achievement_photo_url"]


async def get_is_registered(sm_id: str):
    """Check if a user is registered by social media ID (telegram_id or vk_id)"""
    api_base_url = os.getenv("API_BASE_URL", "http://museum_api:8000")

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{api_base_url}/is-registered/{sm_id}") as response:
            if response.status == 200:
                return await response.json()
            else:
                error_data = await response.json()
                raise Exception(f"API error: {error_data.get('detail', 'Unknown error')}")


async def register(user_data: RegistrationData):
    """Register a new user by sending data to the /register endpoint."""
    api_base_url = os.getenv("API_BASE_URL", "http://museum_api:8000")

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{api_base_url}/register", json=user_data.model_dump()) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_data = await response.json()
                raise Exception(f"API error: {error_data.get('detail', 'Unknown error')}")


async def get_random_history() -> HistoryResponse:
    """Get random history from the museum API."""
    api_base_url = os.getenv("API_BASE_URL", "http://museum_api:8000")

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{api_base_url}/random-history") as response:
            if response.status == 200:
                response_data = await response.json()
                return HistoryResponse(**response_data)
            else:
                error_data = await response.json()
                raise Exception(f"API error: {error_data.get('detail', 'Unknown error')}")
