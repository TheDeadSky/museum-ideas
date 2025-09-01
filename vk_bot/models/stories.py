from pydantic import BaseModel, Field

from models.base import BaseResponse


class HistoryData(BaseModel):
    author: str | None = None
    title: str | None = None
    text: str | None = None
    media_url: str | None = None
    link: str | None = None
    is_anonymous: bool = False
    is_agreed_to_publication: bool = True
    content_type: str = Field(default="text", description="`text`, `audio` or `video`")


class HistoryResponse(BaseResponse):
    history: HistoryData | None = None
