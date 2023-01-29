from datetime import datetime
import json
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
    
    if search:
        s = json.loads(search)
        raffles = [raffle for raffle in raffles if raffle[list(s.keys())[0]] == s[list(s.keys())[0]]]
        return raffles
    else:
        return {'status': 'success', 'results': len(raffles), 'raffles': raffles}