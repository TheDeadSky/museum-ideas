import random
from services.api_service import get_colleagues_stories


async def get_random_story():
    stories = await get_colleagues_stories()
    return random.choice(stories)
