from vkbottle.bot import BotLabeler
from .enter import experience_enter_labeler
from .confirmation import experience_confirmation_labeler
from .anonymity import experience_anonymity_labeler
from .publishing import experience_publishing_labeler

share_experience_labeler = BotLabeler()

share_experience_labeler.load(experience_enter_labeler)
share_experience_labeler.load(experience_confirmation_labeler)
share_experience_labeler.load(experience_anonymity_labeler)
share_experience_labeler.load(experience_publishing_labeler)


__all__ = ["share_experience_labeler"]
