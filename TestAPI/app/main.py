from typing import Union
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db
from sqlalchemy import text

import json

from schema import User as SchemaUser
from schema import Username as SchemaUsername
from schema import Location as SchemaLocation
from schema import QR as SchemaQR
from schema import Tracking as SchemaTracking

from schema import User
from schema import Username
from schema import Location
from schema import QR
from schema import Tracking

from models import User as ModelUser
from models import Username as ModelUsername
from models import Location as ModelLocation
from models import QR as ModelQR
from models import Tracking as ModelTracking

from datetime import datetime, timedelta
import uuid
import random

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url="postgresql://postgres:VeryEasyPassword12398@db:5432/postgres")

@app.get("/")
def read_root():
    return {"Hello": "World"}

#Simple tester function
#should return the ID given
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

#Add a new user
#Requires:
#"UserID" = UUID (for now just using int)
#Example: {"UserID":"1"}
@app.post('/user/add', response_model=SchemaUser)
async def User(User: SchemaUser):
    db_User = ModelUser(UserID=User.UserID)
    db.session.add(db_User)
    db.session.commit()
    return db_User

@app.get('/user/get')
async def User():
    User = db.session.query(ModelUser).all()
    return User


#Add a new username
#Requires:
#"UserID" = UUID (for now just using int)
#Example: {"UserID":"1", "Username": "DylanIsTheBest"}
@app.post('/username/add', response_model=SchemaUsername)
async def Username(User: SchemaUsername):
    db_Username = SchemaUsername(UserID=User.UserID)
    db.session.add(db_Username)
    db.session.commit()
    return db_Username

#Add a new Location
#Requires:
#"LocationID" = UUID (for now just using int)
#"name" = string, the location name
#"URL" = the URL of the website for the location
#Example: {"LocationID":"1", "name":"Hartree Centre", "URL":"www.nowebsiteyet.com/hartree"}
@app.post('/location/add', response_model=SchemaLocation)
async def Location(Location: SchemaLocation):
    db_Location = ModelLocation(LocationID=Location.LocationID,name=Location.name,URL=Location.URL,)
    db.session.add(db_Location)
    db.session.commit()
    return db_Location

@app.get('/location/get')
async def Location():
    Location = db.session.query(ModelLocation).all()
    return Location

#Add a new QR
#Requires:
#"QRID" = UUID (for now just using int)
#"LocationID" = UUID, foreignkey for the location
#Example: {"QRID":"1", "LocationID":"1"}
@app.post('/qr/add', response_model=SchemaQR)
async def QR(QR: SchemaQR):
    db_QR = ModelQR(QRID=QR.QRID,LocationID=QR.LocationID)
    db.session.add(db_QR)
    db.session.commit()
    return db_QR

@app.get('/qr/get')
async def QR():
    QR = db.session.query(ModelQR).all()

    print("test", QR[0].Location)
    return QR

#Add a new Tracking
#Requires:
#"TrackingID" = UUID (for now just using int)
#"UserID" = UUID, foreignkey for the location
#"QRID" = UUID, foreignkey for the location
#"Timestamp" = DateTime, DateTime of tracking event
#Example: {"UserID":"1", "QRID":"1"}
@app.post('/tracking/add', response_model=SchemaTracking)
async def Tracking(Tracking: SchemaTracking):

    user = db.session.query(ModelUser).filter_by(UserID=Tracking.UserID).first()

    print("Debug = ", user)

    if not user:
        db_User = ModelUser(UserID=Tracking.UserID)
        db.session.add(db_User)
        db.session.commit()

    db_Tracking = ModelTracking(TrackingID= str(uuid.uuid4()) ,UserID=Tracking.UserID, QRID=Tracking.QRID)
    db.session.add(db_Tracking)
    db.session.commit()
    return db_Tracking

#random.randint(1, 30)
@app.get('/tracking/random')
async def Tracking():
    db_Tracking = ModelTracking(TrackingID= str(uuid.uuid4()), UserID=str( random.randint(1, 2)) , QRID=str(random.randint(1, 2)))
    db.session.add(db_Tracking)
    db.session.commit()
    return db_Tracking.QRID

@app.get('/tracking/get')
async def Tracking():
    QR = db.session.query(ModelTracking).all()
    return QR

@app.get('/tracking/get1day')
async def Tracking():
    one_day_interval_before = datetime.utcnow() - timedelta(seconds=1)
    print(one_day_interval_before)
    #result = db.session.query(ModelTracking).filter(ModelTracking.UserID == x.UserID).order_by(ModelTracking.Timestamp.desc()).limit(2).subquery()
    QR = db.session.query(ModelTracking).from_statement(text('''
    SELECT
        *
    FROM
        (SELECT DISTINCT  "Tracking"."UserID"  FROM "Tracking" 
    WHERE "Tracking"."Timestamp" >= ' ''' + str(one_day_interval_before)  + ''' ') seenUsers,
    LATERAL
        (SELECT *
        FROM   "Tracking" 
        WHERE  "Tracking"."UserID" = seenUsers."UserID"
        ORDER BY "Tracking"."Timestamp" DESC
        LIMIT 2) l2
    ;
    ''')).all()

    return QR

@app.get('/tracking/getpast')
async def Tracking():
    one_day_interval_before = datetime.utcnow() - timedelta(hours=12)
    print(one_day_interval_before)
    #result = db.session.query(ModelTracking).filter(ModelTracking.UserID == x.UserID).order_by(ModelTracking.Timestamp.desc()).limit(2).subquery()
    QR = db.session.query(ModelTracking).from_statement(text('''
    SELECT
        *
    FROM
        (SELECT DISTINCT  "Tracking"."UserID"  FROM "Tracking" 
    WHERE "Tracking"."Timestamp" >= ' ''' + str(one_day_interval_before)  + ''' ') seenUsers,
    LATERAL
        (SELECT *
        FROM   "Tracking" 
        WHERE  "Tracking"."UserID" = seenUsers."UserID"
        ORDER BY "Tracking"."Timestamp" DESC
        LIMIT 1) l2
    ;
    ''')).all()

    return QR

#Example: {"UserID":"1"}
@app.post('/tracking/onefulluser')
async def Tracking(Tracking: SchemaUser):
    FullHistory = db.session.query(ModelTracking).filter_by(UserID=Tracking.UserID).all()

    FullHistoryList = []

    for x in FullHistory:
        x.Timestamp = str( x.Timestamp )
        FullHistoryList.append(x.as_dict())

    print(str(FullHistoryList))

    return FullHistoryList

