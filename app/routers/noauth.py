from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Response
from pymongo.collection import ReturnDocument
from app import schemas
from app.database import Raffle, User

from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError
from app.serializers.raffleSerializers import raffleListEntity_NoAuth

router = APIRouter()

@router.get("/raffles")
def get_raffles(limit: int = 10, page: int = 1, search: str = ''):
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
    
    raffles = raffleListEntity_NoAuth(Raffle.aggregate(pipeline))

    
        
    return {'status': 'success', 'results': len(raffles), 'raffles': raffles}