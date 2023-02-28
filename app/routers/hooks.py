import json
from datetime import datetime

from fastapi import APIRouter, Depends, Body, status, Request
from pymongo.collection import ReturnDocument
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError

from app.database import Purchase, Raffle
from app.serializers.purchaseSerializers import purchaseEntity
from app.serializers.raffleSerializers import raffleEntity
from app.controllers.paymentController import MP

router = APIRouter()

@router.post("/mp", status_code=status.HTTP_200_OK)
def mp_hook(req_body: dict = Body(...)):
    if req_body["action"] == "payment.updated":
        payment_id = int(req_body["data"]["id"])
        
        p_data = Purchase.find_one({'payment_id': payment_id})
        r_data = Raffle.find_one({'payment_id': payment_id})
        
        mp = MP()
        payment = mp.get_payment(payment_id=payment_id)
        payment_act_status_detail = payment["status_detail"]
        payment_act_status = payment["status"]
        
        if payment_act_status_detail == "accredited" and payment_act_status == "approved":            
            if p_data:
                p_data = purchaseEntity(p_data)
                Purchase.find_one_and_update({'_id': ObjectId(p_data["id"])}, {"$set": {"status": "verified"}})
                
            if r_data:
                r_data = raffleEntity(r_data)
                Raffle.find_one_and_update({'_id': ObjectId(r_data["id"])}, {"$set": {"published": True, "published_at": datetime.utcnow()}})