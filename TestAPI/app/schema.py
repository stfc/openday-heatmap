# build a schema using pydantic
from pydantic import BaseModel

class User(BaseModel):
    UserID: str

    class Config:
        orm_mode = True

class Username(BaseModel):
    UserID: str
    Username: str

    class Config:
        orm_mode = True

class Location(BaseModel):
    LocationID: str
    name: str
    URL: str

    class Config:
        orm_mode = True

class QR(BaseModel):
    QRID: str
    LocationID: str

    class Config:
        orm_mode = True

class Tracking(BaseModel):
    UserID: str
    QRID: str

    class Config:
        orm_mode = True

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}