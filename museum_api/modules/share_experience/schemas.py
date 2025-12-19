from pydantic import BaseModel


class ShareExperienceData(BaseModel):
    sm_id: str
    experience: str
    experience_type: str = "text"
    publish: bool = True
    is_anonymous: bool = True
