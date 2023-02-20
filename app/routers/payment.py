import json

from fastapi import APIRouter, Depends, HTTPException, status, Response

from pymongo.collection import ReturnDocument
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError

from app.database import Purchase
from app.serializers.purchaseSerializers import purchaseResponseEntity
from app.oauth2 import require_user
from app.controllers.paymentController import MP

def paymentResponse(payment) -> dict:
    return {
        "status": payment["status"],
        "status_detail": payment["status_detail"]
    }

router = APIRouter()


@router.get("/")
def get_payments(limit: int = 30, page: int = 1, only_my: bool = True, search: str = "", user_id: str = Depends(require_user)):
    mp = MP()
    payments = mp.get_payment()
    
    purchases = []
    
    for payment in payments:
        purchase = purchaseResponseEntity(Purchase.find_one({"payment_id": payment["payment_id"]}))
        purchase["payment"] = payment
        
        purchases.append(purchase)
    
    if search:
        search = json.loads(search)
    
    
    return {"status": "success", "size": len(payments), "payments": purchases}

    
@router.get("/{id}")
def get_payment(id: int, user_id: str = Depends(require_user)):
    mp = MP()
    payment = mp.get_payment(payment_id=id)