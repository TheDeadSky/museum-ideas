from aiogram import Router
from aiogram.types import Message

from menus import YES_NO_MENU


registration_router = Router()


@registration_router.message()
async def get_user_name(message: Message):
    name = message.text

    print(f"Saving {name=} to db...")  # send to API for saving

    await message.answer("Вы работаете в музее?", reply_markup=YES_NO_MENU)
    # Next state
