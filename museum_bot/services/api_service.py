import json


async def get_self_support_course():
    # async with aiohttp.ClientSession() as session:
    #     async with session.get("https://api.example.com/self-support-course") as response:
    #         return await response.json()

    with open("src/self_support_course.json", "r", encoding="utf-8") as file:
        return json.load(file)


async def get_colleagues_stories():
    with open("src/colleagues_stories.json", "r", encoding="utf-8") as file:
        return json.load(file)


async def get_text_from_db(text_key: str):
    with open("src/texts_in_db.json", "r", encoding="utf-8") as file:
        return json.load(file)[text_key]


async def get_achievement_photo_url():
    with open("src/achievement_photo_url.json", "r", encoding="utf-8") as file:
        return json.load(file)["achievement_photo_url"]
