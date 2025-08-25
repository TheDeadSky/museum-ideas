from vkbottle.bot import Message

from models.experience import ShareExperienceData
from services.api_service import send_experience
from menus import TO_MAIN_MENU_BUTTON
from states.general_states import GeneralStates
from settings import state_dispenser


async def submit_share_experience(message: Message, data: dict):
    valid_data = None

    valid_data = ShareExperienceData(**{
        "sm_id": str(message.peer_id),
        **data
    })

    response = await send_experience(valid_data)
    print(response)

    state_dispenser.set(
        message.peer_id,
        GeneralStates.MAIN_MENU
    )

    await message.answer(
        response["message"],
        keyboard=TO_MAIN_MENU_BUTTON
    )
