import json

from fastapi import APIRouter, Depends, HTTPException, status, Response

from pymongo.collection import ReturnDocument
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError

from app.database import Purchase
from app.serializers.purchaseSerializers import purchaseResponseEntity
from app.serializers.paymentSerializers import paymentListEntity, paymentEntity
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
    payments = paymentListEntity(payments["results"])
        
    if search:
        search = json.loads(search)
        
        payments = [payment for payment in payments if search]
    
    
    return {"status": "success", "size": len(payments), "payments": payments}

    
@router.get("/{id}")
def get_payment(id: int, user_id: str = Depends(require_user)):
    mp = MP()
    payment = mp.get_payment(payment_id=id)
    payment = paymentEntity(payment)
    
    if payment:
        return {"status": "success", "payments": paymentEntity(payment)}
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            detail=f"Payment {id} not found.")