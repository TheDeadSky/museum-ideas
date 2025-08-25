from vkbottle import BaseStateGroup


class ShareExperienceStates(BaseStateGroup):
    SHARE_EXPERIENCE = "share-experience"
    CONFIRMATION = "confirmation"
    ANONYMITY = "anonymity"
    EXPERIENCE_INPUT = "experience-input"
    PUBLISHING = "publishing"


__all__ = ["ShareExperienceStates"]
