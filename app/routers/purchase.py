import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Response
from pymongo.collection import ReturnDocument
from app import schemas
from app.database import User, Purchase, Raffle

from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError
from app.serializers.userSerializers import userEntity
from app.serializers.purchaseSerializers import purchaseEntity, purchaseListEntity, purchaseResponseEntity
from app.serializers.raffleSerializers import raffleEntity
from app.controllers.purchaseController import auto_bet, check_bets
from app.controllers.paymentController import MP

from .. import schemas

from app.oauth2 import require_user, RoleChecker
from app.config import settings

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
    user = userEntity(User.find_one({"_id": purchase.user}))
    
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
    
    raffle_title = raffle["title"]
    
    payment_data = {
        "total_value": purchase.quantity * raffle["quota_value"],
        "description": f"Compra de {purchase.quantity} cotas para a campanha {raffle_title}.",
        "payment_method": "pix",
        "reserve_time": settings.PURCHASE_PAYMENT_EXPIRE_TIME,
        "created_at": purchase.purchased_at,
        "client_fname": (user["name"].split(" "))[0],
        "client_lname": (user["name"].split(" "))[-1]        
    }
    
    if user["role"] == "cli":
        payment_data["client_email"] = "huandersonferreira7@gmail.com"
    
    if len(raffle["promotion"]) == 1 and purchase.quantity >= (raffle["promotion"][0])["raffle_qtd"]:
        payment_data["discount_value"] = (raffle["promotion"][0])["raffle_discount"]
    
    if len(raffle["promotion"]) > 1:
        for idx, promo in enumerate(raffle["promotion"]):
            if promo["raffle_qtd"] <= purchase.quantity and (raffle["promotion"][idx+1])["raffle_qtd"] >= purchase.quantity:
                payment_data["discount_value"] = promo["raffle_discount"]
                
    try:
        payment = MP()
        payment_res = payment.create_payment(payment_data)
        
        purchase.payment_id = payment_res["id"]
        try:
            result = Purchase.insert_one(purchase.dict())
                
            return {
                'status': 'success', 
                'purchase': {
                    "id": str(result.inserted_id),
                    "bet": purchase.bet
                },
                "payment": {
                    "id": payment_res["id"],
                    "qrcode": payment_res["point_of_interaction"]["transaction_data"]["qr_code"],
                    "qr_code_base64": payment_res["point_of_interaction"]["transaction_data"]["qr_code_base64"]
                }
            }
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Fail")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Fail to process payment")                

        
@router.get("/")
def get_purchases(limit: int = 10, page: int = 1, only_my: bool = False, search: str = '', user_id: str = Depends(require_user)):
    skip = (page - 1) * limit
    pipeline = [
        {'$match': {}},
        {'$lookup': {'from': 'users', 'localField': 'user', 'foreignField': '_id', 'as': 'user'}},
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