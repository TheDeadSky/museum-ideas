from io import BytesIO
import logging
from typing import BinaryIO
from aiogram.fsm.scene import Scene, on
from aiogram.types import CallbackQuery, User, Voice
import aiohttp

from models.experience import ShareExperienceData
from services.api_service import send_experience
from menus import TO_MAIN_MENU_BUTTON


class SubmitShareExperienceScene(Scene, state="share-experience-submit"):
    @on.message.enter()
    async def on_enter(self, message: CallbackQuery, from_user: User = None):
        data = await self.wizard.get_data()

        valid_data = None

        if isinstance(data["experience"], Voice):
            file_id = data["experience"].file_id
            file_binary: BinaryIO = BytesIO()
            logging.info(f"Downloading file {data['experience']}")

            voice_file = await message.bot.get_file(file_id)
            await message.bot.download_file(voice_file.file_path, file_binary)

            upload_url = "https://ideasformuseums.com/tgbot/upload-audio/"
            async with aiohttp.ClientSession() as session:
                form = aiohttp.FormData()
                form.add_field(
                    name="audio_file",
                    value=file_binary,
                    filename="voice.ogg",
                    content_type="audio/ogg"
                )
                async with session.post(upload_url, data=form) as resp:
                    logging.info(f"Upload response:    {await resp.text()}")
                    upload_response = await resp.json(content_type="text/html")

            if "filename" in upload_response:
                get_audio_url = "https://ideasformuseums.com/tgbot/get-audio/?filename="

                data["experience"] = get_audio_url + upload_response["filename"]
                data["experience_type"] = "audio"

                valid_data = ShareExperienceData(
                    **{
                        "sm_id": str(from_user.id),
                        **data
                    }
                )
            else:
                await message.edit_text(
                    upload_response.get("error", "Unknown upload error"),
                    reply_markup=TO_MAIN_MENU_BUTTON
                )
                return
        else:
            valid_data = ShareExperienceData(**{
                "sm_id": str(from_user.id),
                **data
            })

        response = await send_experience(valid_data)
        print(response)

        await message.edit_text(
            response["message"],
            reply_markup=TO_MAIN_MENU_BUTTON
        )

    @on.callback_query.enter()
    async def on_enter_callback(self, callback: CallbackQuery):
        await callback.answer()
        await self.on_enter(callback.message, callback.from_user)
