# build a schema using pydantic
from uuid import UUID

from pydantic import BaseModel


class UserRequest(BaseModel):
    # Separated into UserRequest as we only want the nickname
    Nickname: str


class User(UserRequest):
    UserID: UUID

    class Config:
        orm_mode = True


class FeedbackRequest(BaseModel):
    QRID: int
    EmojiRating: str
    Thoughts: str
    Improvements: str


class Location(BaseModel):
    LocationID: str
    name: str
    URL: str

    class Config:
        orm_mode = True


class QR(BaseModel):
    QRID: int
    LocationID: str

    class Config:
        orm_mode = True


class Tracking(BaseModel):
    UserID: UUID
    QRID: int

    class Config:
        orm_mode = True

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
