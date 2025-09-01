from vkbottle.bot import MessageEvent

from models.experience import ShareExperienceData
from services.api_service import send_experience
from menus import TO_MAIN_MENU_BUTTON
from states.general_states import GeneralStates
from settings import state_dispenser


async def submit_share_experience(event: MessageEvent, data: dict):
    valid_data = None

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
