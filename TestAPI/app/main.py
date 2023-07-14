import random
import uuid
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db
from sqlalchemy import text

from models import QR as ModelQR
from models import Feedback as ModelFeedback
from models import Location as ModelLocation
from models import Tracking as ModelTracking
from models import User as ModelUser
from schema import QR as SchemaQR
from schema import FeedbackRequest
from schema import Location as SchemaLocation
from schema import Tracking as SchemaTracking
from schema import User as SchemaUser
from schema import UserRequest

app = FastAPI()

app.add_middleware(
    DBSessionMiddleware,
    db_url="postgresql://postgres:VeryEasyPassword12398@db:5432/postgres",
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


# Simple tester function
# should return the ID given
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}


@app.post("/users", response_model=SchemaUser, tags=["Users"])
async def add_user(user: UserRequest):
    """Add a new user."""
    db_User = ModelUser(UserID=uuid.uuid4(), Nickname=user.Nickname)
    db.session.add(db_User)
    db.session.commit()
    return db_User


@app.get("/users", response_model=SchemaUser, tags=["Users"])
async def find_user_by_nickname(nickname: str):
    """
    Find a specific user from a nickname.

    Will return 404 if a user isn't found.
    """
    if user := (
        db.session.query(ModelUser).filter(ModelUser.Nickname == nickname).one_or_none()
    ):
        return user

    raise HTTPException(status_code=404, detail="User not found")


@app.get("/users/{user_id}", response_model=SchemaUser, tags=["Users"])
async def get_user(user_id: uuid.UUID):
    """
    Find a specific user using their user ID.

    Will return 404 if a user isn't found.
    """
    if user := (
        db.session.query(ModelUser).filter(ModelUser.UserID == user_id).one_or_none()
    ):
        return user

    raise HTTPException(status_code=404, detail="User not found")


@app.get("/user/get", response_model=list[SchemaUser], tags=["Users"])
async def get_users():
    return db.session.query(ModelUser).all()


@app.post("/users/{user_id}/feedback", tags=["Users"])
async def set_feedback(user_id: uuid.UUID, feedback: FeedbackRequest):
    """Set feedback for a specific user."""
    db_feedback = ModelFeedback(
        QRID=feedback.QRID,
        UserID=user_id,
        EmojiRating=feedback.EmojiRating,
        Thoughts=feedback.Thoughts,
        Improvements=feedback.Improvements,
    )
    db.session.add(db_feedback)
    db.session.commit()
    return db_feedback


# Add a new Location
# Requires:
# "LocationID" = UUID (for now just using int)
# "name" = string, the location name
# "URL" = the URL of the website for the location
# Example: {"LocationID":"1", "name":"Hartree Centre", "URL":"www.nowebsiteyet.com/hartree"}
@app.post("/location/add", response_model=SchemaLocation, tags=["Locations"])
async def add_location(Location: SchemaLocation):
    db_Location = ModelLocation(
        LocationID=Location.LocationID,
        name=Location.name,
        URL=Location.URL,
    )
    db.session.add(db_Location)
    db.session.commit()
    return db_Location


@app.get("/location/get", tags=["Locations"])
async def get_location():
    return db.session.query(ModelLocation).all()


# Add a new QR
# Requires:
# "QRID" = UUID (for now just using int)
# "LocationID" = UUID, foreignkey for the location
# Example: {"QRID":"1", "LocationID":"1"}
@app.post("/qr/add", response_model=SchemaQR, tags=["QR"])
async def add_qr(QR: SchemaQR):
    db_QR = ModelQR(QRID=QR.QRID, LocationID=QR.LocationID)
    db.session.add(db_QR)
    db.session.commit()
    return db_QR


@app.get("/qr/get", tags=["QR"])
async def get_qr():
    QR = db.session.query(ModelQR).all()

    print("test", QR[0].Location)
    return QR


# Add a new Tracking
# Requires:
# "TrackingID" = UUID (for now just using int)
# "UserID" = UUID, foreignkey for the location
# "QRID" = UUID, foreignkey for the location
# "Timestamp" = DateTime, DateTime of tracking event
# Example: {"UserID":"1", "QRID":"1"}
@app.post("/tracking/add", response_model=SchemaTracking, tags=["Tracking"])
async def add_tracking(Tracking: SchemaTracking):
    user = db.session.query(ModelUser).filter_by(UserID=Tracking.UserID).first()

    print("Debug = ", user)

    if not user:
        db_User = ModelUser(UserID=Tracking.UserID)
        db.session.add(db_User)
        db.session.commit()

    db_Tracking = ModelTracking(
        TrackingID=str(uuid.uuid4()), UserID=Tracking.UserID, QRID=Tracking.QRID
    )
    db.session.add(db_Tracking)
    db.session.commit()
    return db_Tracking


# random.randint(1, 30)
@app.get("/tracking/random", tags=["Tracking"])
async def add_random_tracking():
    db_Tracking = ModelTracking(
        TrackingID=str(uuid.uuid4()),
        UserID=str(random.randint(1, 2)),
        QRID=str(random.randint(1, 2)),
    )
    db.session.add(db_Tracking)
    db.session.commit()
    return db_Tracking.QRID


@app.get("/tracking/get", tags=["Tracking"])
async def get_tracking():
    QR = db.session.query(ModelTracking).all()
    return QR


@app.get("/tracking/get1day", tags=["Tracking"])
async def get_same_day_tracking():
    one_day_interval_before = datetime.utcnow() - timedelta(seconds=1)
    print(one_day_interval_before)
    # result = db.session.query(ModelTracking).filter(ModelTracking.UserID == x.UserID).order_by(ModelTracking.Timestamp.desc()).limit(2).subquery()
    QR = (
        db.session.query(ModelTracking)
        .from_statement(
            text(
                """
    SELECT
        *
    FROM
        (SELECT DISTINCT  "Tracking"."UserID"  FROM "Tracking" 
    WHERE "Tracking"."Timestamp" >= ' """
                + str(one_day_interval_before)
                + """ ') seenUsers,
    LATERAL
        (SELECT *
        FROM   "Tracking" 
        WHERE  "Tracking"."UserID" = seenUsers."UserID"
        ORDER BY "Tracking"."Timestamp" DESC
        LIMIT 2) l2
    ;
    """
            )
        )
        .all()
    )

    return QR


@app.get("/tracking/getpast", tags=["Tracking"])
async def get_past_tracking():
    one_day_interval_before = datetime.utcnow() - timedelta(hours=12)
    print(one_day_interval_before)
    # result = db.session.query(ModelTracking).filter(ModelTracking.UserID == x.UserID).order_by(ModelTracking.Timestamp.desc()).limit(2).subquery()
    QR = (
        db.session.query(ModelTracking)
        .from_statement(
            text(
                """
    SELECT
        *
    FROM
        (SELECT DISTINCT  "Tracking"."UserID"  FROM "Tracking" 
    WHERE "Tracking"."Timestamp" >= ' """
                + str(one_day_interval_before)
                + """ ') seenUsers,
    LATERAL
        (SELECT *
        FROM   "Tracking" 
        WHERE  "Tracking"."UserID" = seenUsers."UserID"
        ORDER BY "Tracking"."Timestamp" DESC
        LIMIT 1) l2
    ;
    """
            )
        )
        .all()
    )

    return QR


# Example: {"UserID":"1"}
@app.post("/tracking/onefulluser", tags=["Tracking"])
async def get_user_tracking(Tracking: SchemaUser):
    FullHistory = (
        db.session.query(ModelTracking).filter_by(UserID=Tracking.UserID).all()
    )

    FullHistoryList = []

    for x in FullHistory:
        x.Timestamp = str(x.Timestamp)
        FullHistoryList.append(x.as_dict())

    print(FullHistoryList)

    return FullHistoryList
