import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Response
from pymongo.collection import ReturnDocument
from app import schemas
from app.database import User, Purchase, Raffle

from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError
from app.serializers.purchaseSerializers import purchaseEntity, purchaseListEntity, purchaseResponseEntity
from app.serializers.raffleSerializers import raffleEntity
from app.controllers.purchaseController import auto_bet, check_bets

from .. import schemas, oauth2

from app.oauth2 import require_user, RoleChecker

allow_admin = RoleChecker(["admin"])
allow_user = RoleChecker(["user"])

router = APIRouter()

@router.post(
    "/{slug}", 
    status_code=status.HTTP_201_CREATED
)
def create_purchase(purchase: schemas.CreatePurchaseSchema, slug: str, user_id: str = Depends(require_user)):
        
    purchase.user = ObjectId(user_id)
    purchase.purchased_at = datetime.utcnow()
    purchase.raffle = slug
    
    
    raffle = raffleEntity(Raffle.find_one({"slug": slug}))
    
    if purchase.betting_method == "auto":
        purchase.bet = auto_bet(raffle["selected_bets"], raffle["quantity"], purchase.quantity)
    
    if purchase.betting_method == "manual":
        bet_validation = check_bets(slug, purchase.bet)
        if bet_validation:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail={"msg":f"This follow bets are not valid.", "content": bet_validation})            
    
    new_sorted_bets = { "$set": { 'selected_bets': [*raffle["selected_bets"], *purchase.bet]}}
    Raffle.find_one_and_update(
        {'_id': ObjectId(raffle["id"])}, new_sorted_bets, return_document=ReturnDocument.AFTER
    )
    
    try:
        result = Purchase.insert_one(purchase.dict())
        
        return {'status': 'success', 'purchase': {"id": str(result.inserted_id), "bet": purchase.bet}}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409,
                            detail=f"Fail")
        
@router.get("/")
def get_purchases(limit: int = 10, page: int = 1, only_my: bool = False, search: str = '', user_id: str = Depends(require_user)):
    skip = (page - 1) * limit
    pipeline = [
        {'$match': {}},
        {'$lookup': {'from': 'users', 'localField': 'user', 'foreignField': '_id', 'as': 'user'}},
        {'$lookup': {'from': 'raffles', 'localField': 'raffle', 'foreignField': '_id', 'as': 'raffle'}},
        {'$unwind': '$user'},
        {
            '$skip': skip
        }, {
            '$limit': limit
        }
    ]
    
    purchases = purchaseListEntity(Purchase.aggregate(pipeline))
    
    if search:
        s = json.loads(search)
        purchases = [purchase for purchase in purchases if purchase[list(s.keys())[0]] == s[list(s.keys())[0]]]

    else:    
        if only_my:
            purchases = [purchase for purchase in purchases if purchase["user"]["id"] == user_id]
        
    return {'status': 'success', 'results': len(purchases), 'purchases': purchases}

@router.get("/{id}")
def get_purchase(id: str, user_id: str = Depends(require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
        
    pipeline = [
        {'$match': {'_id': ObjectId(id)}},
        {'$lookup': {'from': 'users', 'localField': 'user','foreignField': '_id', 'as': 'user'}},
        {'$unwind': '$user'},
    ]
    
    db_cursor = Purchase.aggregate(pipeline)
    results = list(db_cursor)
        
    if len(results) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No purchase with this id: {id} found")
        
    purchase = purchaseListEntity(results)[0]
    
    return purchase


@router.put(
    "/{id}", 
    dependencies=[Depends(allow_admin)]
)
def update_purchase(id: str, payload: schemas.PurchaseUpdateSchema, user_id: str = Depends(require_user)):
    
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
        
    updated_purchase = Purchase.find_one_and_update(
        {'_id': ObjectId(id)}, {'$set': payload.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER
    )
    
    if not updated_purchase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No purchase with this id: {id} found')
        
    return purchaseEntity(updated_purchase)


@router.delete(
    "/{id}", 
    dependencies=[Depends(allow_admin)]
)
def delete_purchase(id: str, user_id: str = Depends(require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
    purchase = Purchase.find_one_and_delete({'_id': ObjectId(id)})
    if not purchase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No purchase with this id: {id} found')
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)