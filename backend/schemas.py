from pydantic import BaseModel, HttpUrl, Field

class YoutuberBase(BaseModel):
    username: str = Field(..., min_length=1)
    link: HttpUrl
    email: str | None = None
    subscribers: int | None = None
    genre: str | None = None

class YoutuberCreate(YoutuberBase):
    pass

class YoutuberRead(YoutuberBase):
    id: int

    class Config:
        from_attributes = True  # required in Pydantic v2
