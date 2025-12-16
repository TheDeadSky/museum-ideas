from vkbottle.bot import MessageEvent

from models.experience import ShareExperienceData
from services.api_service import send_experience
from menus import TO_MAIN_MENU_BUTTON
from services.cloud_storage_service import upload_audio_file
from services.vk_downolad_service import download_voice_audio
from states.general_states import GeneralStates
from settings import state_dispenser


async def submit_share_experience(event: MessageEvent, data: dict):
    if data['experience_type'] == "audio":
        file: bytes = await download_voice_audio(data['experience'])
        file_url = await upload_audio_file(file)
        data["experience"] = file_url


    valid_data = ShareExperienceData(**{
        "sm_id": str(event.peer_id),
        **data
    })

    response = await send_experience(valid_data)
    print(response)

    await state_dispenser.set(
        event.peer_id,
        GeneralStates.MAIN_MENU
    )

    await event.send_message(
        response["message"],
        keyboard=TO_MAIN_MENU_BUTTON.get_json()
    )
