from vkbottle.bot import BotLabeler

from . import (
    start,
    name_input,
    is_museum_worker,
    which_museum_input,
    occupation_input
)

registration_labeler = BotLabeler()


start.init(registration_labeler)
name_input.init(registration_labeler)
is_museum_worker.init(registration_labeler)
which_museum_input.init(registration_labeler)
occupation_input.init(registration_labeler)

__all__ = ["registration_labeler"]
