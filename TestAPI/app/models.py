from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.types import UUID, Integer

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = "User"

    UserID = Column(UUID, primary_key=True)
    Nickname = Column(String, unique=True, nullable=False)


class Location(Base):
    __tablename__ = "Location"

    LocationID = Column(String, primary_key=True)
    name = Column(String)
    URL = Column(String)


class Feedback(Base):
    __tablename__ = "Feedback"

    FeedbackID = Column(Integer, primary_key=True)
    # Use QRID for feedback to avoid an unnecessary API call to find the location ID 
    QRID = Column(Integer, ForeignKey("QR.QRID"))
    UserID = Column(UUID, ForeignKey("User.UserID"))
    EmojiRating = Column(String, nullable=False)  # TODO: Could be an enum
    Thoughts = Column(String, nullable=False)  # What you thought was good?
    Improvements = Column(String, nullable=False)  # What you would improve

    Location = relationship("QR")
    User = relationship("User")


class QR(Base):
    __tablename__ = "QR"

    QRID = Column(Integer, primary_key=True)
    LocationID = Column(String, ForeignKey("Location.LocationID"))

    Location = relationship("Location")


class Tracking(Base):
    __tablename__ = "Tracking"

    TrackingID = Column(String, primary_key=True)
    UserID = Column(UUID, ForeignKey("User.UserID"))
    QRID = Column(Integer, ForeignKey("QR.QRID"))
    Timestamp = Column(DateTime(timezone=True), default=func.now())

    User = relationship("User")
    QR = relationship("QR")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
