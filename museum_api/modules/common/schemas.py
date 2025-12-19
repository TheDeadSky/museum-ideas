from typing import List

from pydantic import BaseModel

from schemas import BaseResponse
from shared.models import ApiResponse


class MessageForAll(BaseModel):
    message: str
    platform: str = "all"


class MessageForAllResponse(BaseResponse):
    platform: str = "all"
    tg_response: ApiResponse | None = None
    vk_response: ApiResponse | None = None


class TgAPIMessageForAll(BaseModel):
    message: str
    tg_ids: List[int]
