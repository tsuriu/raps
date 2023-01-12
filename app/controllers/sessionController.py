from datetime import datetime

from fastapi import Depends, Request
from app.serializers.sessionSerializers import sessionEntity, sessionListEntity
from app.database import Session

from .. import schemas

def create_session(session: schemas.SessionBaseSchema, request: Request):
    session.created_at = datetime.utcnow()
    
    try:
        result = Session.insert_one(session.dict())
        pipeline = [
            {'$match': {'_id': result.inserted_id}},
            {'$lookup': {'from': 'users', 'localField': 'user',
                         'foreignField': '_id', 'as': 'user'}},
            {'$unwind': '$user'},
        ]
        result = sessionListEntity(Session.aggregate(pipeline))[0]
        
        return {'status': 'success', 'session': result["id"]}
    except:
        pass
    

def get_sessions():
    pass


def delete_session():
    pass