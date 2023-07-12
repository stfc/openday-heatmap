from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Sequence
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

Base  = declarative_base()
metadata = Base.metadata

class User(Base):
    __tablename__ = "user"

    UserID = Column(String, primary_key=True)

class Username(Base):
    __tablename__ = "username"

    username = Column(String, primary_key=True)
    UserID = Column(String, ForeignKey("user.UserID"))

    User = relationship("User")


class Location(Base):
    __tablename__ = "Location"

    LocationID = Column(String, primary_key=True)
    name = Column(String)
    URL = Column(String)

class QR(Base):
    __tablename__ = "QR"

    QRID = Column(String, primary_key=True)
    LocationID = Column(String, ForeignKey("Location.LocationID"))

    Location = relationship("Location")

class Tracking(Base):
    __tablename__ = "Tracking"

    TrackingID = Column(String, primary_key=True)
    UserID = Column(String, ForeignKey("user.UserID"))
    QRID = Column(String, ForeignKey("QR.QRID"))
    Timestamp = Column(DateTime(timezone=True), default=func.now())

    User = relationship("User")
    QR = relationship("QR")

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}