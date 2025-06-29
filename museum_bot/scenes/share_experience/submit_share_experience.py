from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery

from models.experience import ShareExperienceData
from services.api_service import send_experience
from menus import TO_MAIN_MENU_BUTTON


class SubmitShareExperienceScene(Scene, state="share-experience-submit"):
    @on.message.enter()
    async def on_enter(self, message: CallbackQuery):
        data = await self.wizard.get_data()

        valid_data = ShareExperienceData(**{
            **data,
            "sm_id": message.from_user.id
        })

        response = await send_experience(valid_data)
        print(response)

        await message.answer(
            response["message"],
            reply_markup=TO_MAIN_MENU_BUTTON
        )

    @on.callback_query.enter()
    async def on_enter_callback(self, callback: CallbackQuery):
        await callback.answer()
        await self.on_enter(callback.message)
