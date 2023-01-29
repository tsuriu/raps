from datetime import datetime
import json
from fastapi import APIRouter, Depends, HTTPException, status, Response
from pymongo.collection import ReturnDocument
from app import schemas
from app.database import Raffle

from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError
from app.serializers.raffleSerializers import prizeEntity, raffleResponseEntity, raffleEntity, raffleListEntity

from app.database import User
from .. import schemas, oauth2

from app.oauth2 import require_user, RoleChecker

allow_raffle_creation = RoleChecker(["admin","user"])


router = APIRouter()

@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(allow_raffle_creation)]
)
def create_raffle(raffle: schemas.CreateRaffleSchema, user_id: str = Depends(require_user)):
    raffle.user = ObjectId(user_id)
    raffle.created_at = datetime.utcnow()
    raffle.updated_at = raffle.created_at
    
    check_slug = False #get_raffles(search=str({"slug": raffle.slug}), only_my=False)
    
    if not raffle.slug:
        raffle.slug = ((raffle.title).lower()).replace(" ", "-")
    
    if raffle.slug and check_slug:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Raffle with title: '{raffle.slug}' already exists")
    
    try:
        result = Raffle.insert_one(raffle.dict())
        pipeline = [
            {'$match': {'_id': result.inserted_id}},
            {'$lookup': {'from': 'users', 'localField': 'user',
                         'foreignField': '_id', 'as': 'user'}},
            {'$unwind': '$user'},
        ]
        raffle = raffleListEntity(Raffle.aggregate(pipeline))[0]
        
        return {'status': 'success', 'raffle': raffle}
        
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Raffle with title: '{raffle.title}' already exists")
        
        
@router.get("/")
def get_raffles(limit: int = 10, page: int = 1, only_my: bool = True, search: str = "", user_id: str = Depends(require_user)):
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
    
    if search:
        s = json.loads(search)
        raffles = [raffle for raffle in raffles if raffle[list(s.keys())[0]] == s[list(s.keys())[0]]]
        return raffles
    else:    
        if only_my:
            raffles = [raffle for raffle in raffles if raffle["user"]["id"] == user_id]
        
        return {'status': 'success', 'results': len(raffles), 'raffles': raffles}


@router.get("/{id}")
def get_raffle(id: str, user_id: str = Depends(require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
        
    pipeline = [
        {'$match': {'_id': ObjectId(id)}},
        {'$lookup': {'from': 'users', 'localField': 'user',
                     'foreignField': '_id', 'as': 'user'}},
        {'$unwind': '$user'},
    ]
    
    db_cursor = Raffle.aggregate(pipeline)
    results = list(db_cursor)
        
    if len(results) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No raffle with this id: {id} found")
        
    raffle = raffleListEntity(results)[0]
    
    return raffle


@router.put(
    "/{id}",
    dependencies=[Depends(allow_raffle_creation)]
)
def update_raffle(id: str, payload: schemas.RaffleUpdateSchema, user_id: str = Depends(require_user)):
    
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
        
    raffle = raffleEntity(Raffle.find_one({"_id": ObjectId(id)}))
    
    if user_id != raffle["user"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Operation not permitted")
        
    payload.updated_at = datetime.utcnow()        
    payload_run = dict(payload)
    
    if "published" in payload_run.keys() and raffle["published"] == False and payload_run["published"] == True:
        payload.published_at = datetime.utcnow()
        
            
    updated_raffle = Raffle.find_one_and_update(
        {'_id': ObjectId(id)}, {'$set': payload.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER
    )
    
    if not updated_raffle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No raffle with this id: {id} found')
        
    return raffleEntity(updated_raffle)



@router.delete(
    "/{id}",
    dependencies=[Depends(allow_raffle_creation)]
)
def delete_raffle(id: str, user_id: str = Depends(require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
    raffle = Raffle.find_one_and_delete({'_id': ObjectId(id)})
    if not raffle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No raffle with this id: {id} found')
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)