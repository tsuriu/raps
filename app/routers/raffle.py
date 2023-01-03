from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Response
from pymongo.collection import ReturnDocument
from app import schemas
from app.database import Raffle

from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError
from app.serializers.raffleSerializers import raffleResponseEntity, raffleEntity, raffleListEntity

from app.database import User
from .. import schemas, oauth2

from app.oauth2 import require_user


router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_raffle(raffle: schemas.CreateRaffleSchema, user_id: str = Depends(require_user)):
    raffle.user = ObjectId(user_id)
    raffle.created_at = datetime.utcnow()
    raffle.updated_at = raffle.created_at
    
    try:
        result = Raffle.insert_one(raffle.dict())
        pipeline = [
            {'$match': {'_id': result.inserted_id}},
            {'$lookup': {'from': 'users', 'localField': 'user',
                         'foreignField': '_id', 'as': 'user'}},
            {'$unwind': '$user'},
        ]
        raffleListEntity(Raffle.aggregate(pipeline))[0]
        
        return {'status': 'success'}
        
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Raffle with title: '{raffle.title}' already exists")
        
@router.get('/')
def get_raffles(limit: int = 10, page: int = 1, search: str = '', user_id: str = Depends(require_user)):
    skip = (page - 1) * limit
    pipeline = [
        {'$match': {}},
        {'$lookup': {'from': 'users', 'localField': 'user',
                     'foreignField': '_id', 'as': 'user'}},
        {'$unwind': '$user'},
        {
            '$skip': skip
        }, {
            '$limit': limit
        }
    ]
    raffles = raffleListEntity(Raffle.aggregate(pipeline))
    return {'status': 'success', 'results': len(raffles), 'raffles': raffles}