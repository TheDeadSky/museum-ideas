from vkbottle.bot import BotLabeler
from .enter import get_support_enter_labeler
from .show_colleagues_stories import colleagues_stories_labeler
from .self_support_course import self_support_course_labeler

get_support_labeler = BotLabeler()

get_support_labeler.load(get_support_enter_labeler)
get_support_labeler.load(colleagues_stories_labeler)
get_support_labeler.load(self_support_course_labeler)

__all__ = ["get_support_labeler"]
