from enum import StrEnum


class ExperienceType(StrEnum):
    TEXT = "text"
    AUDIO = "audio"


class ExperienceStatus(StrEnum):
    MODERATION = "moderation"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
