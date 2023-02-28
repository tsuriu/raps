from datetime import datetime
import json
from fastapi import APIRouter, Depends, HTTPException, status, Response
from pymongo.collection import ReturnDocument
from app import schemas
from app.database import Raffle

from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError
from app.serializers.raffleSerializers import prizeEntity, raffleResponseEntity, raffleEntity, raffleListEntity
from app.serializers.userSerializers import userEntity

from app.controllers.paymentController import MP
from app.controllers.parametersController import calc_raffle_taxes

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
    raffle.available_bet = raffle.quantity
    
    user = userEntity(User.find_one({"_id": raffle.user}))
    
    check_slug = False #get_raffles(search=str({"slug": raffle.slug}), only_my=False)
    
    if not raffle.slug:
        raffle.slug = ((raffle.title).lower()).replace(" ", "-")
    
    if raffle.slug and check_slug:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Raffle with title: '{raffle.slug}' already exists")
        
        
    raffle_publish_tax, raffle_total_value_return = calc_raffle_taxes(raffle.dict())
    raffle_publish_payment_lifetime = 1
    
    raffle.publish_tax = raffle_publish_tax
    raffle.total_value_return = raffle_total_value_return
    
    payment_data = {
        "total_value": raffle_publish_tax,
        "description": f" Taxa de publicao da rifa {raffle.title}.",
        "payment_method": "pix",
        "reserve_time": raffle_publish_payment_lifetime,
        "created_at": raffle.created_at,
        "client_fname": (user["name"].split(" "))[0],
        "client_lname": (user["name"].split(" "))[-1],
        "client_email": user["email"]        
    }
    
    try:
        payment = MP()
        payment_res = payment.create_payment(payment_data)
        
        raffle.payment_id = payment_res["id"]
        
        result = Raffle.insert_one(raffle.dict())
        pipeline = [
            {'$match': {'_id': result.inserted_id}},
            {'$lookup': {'from': 'users', 'localField': 'user',
                        'foreignField': '_id', 'as': 'user'}},
            {'$unwind': '$user'},
        ]
        raffle = raffleListEntity(Raffle.aggregate(pipeline))[0]
        
        return {
            'status': 'success', 
            'raffle': raffle,
            "payment": {
                "id": payment_res["id"],
                "qrcode": payment_res["point_of_interaction"]["transaction_data"]["qr_code"],
                "qr_code_base64": payment_res["point_of_interaction"]["transaction_data"]["qr_code_base64"],
                "total_paid_amount": payment_res["transaction_details"]["total_paid_amount"],
                "transaction_amount": payment_res["transaction_amount"],
                "date_of_expiration": payment_res["date_of_expiration"]
            }                
        }
            
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        
        
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
        
    
    user = userEntity(User.find_one({'_id': ObjectId(str(user_id))}))
    raffle = raffleEntity(Raffle.find_one({"_id": ObjectId(id)}))
    
    if (user_id != raffle["user"] and user["role"] == "user") or user["role"] != "admin":
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