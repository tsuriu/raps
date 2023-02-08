import json

from fastapi import APIRouter, Depends, HTTPException, status, Response

from pymongo.collection import ReturnDocument

from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError

from app.oauth2 import require_user
from app.controllers.paymentController import MP

router = APIRouter()


@router.get("/")
def get_payments(limit: int = 30, page: int = 1, only_my: bool = True, search: str = "", user_id: str = Depends(require_user)):
    pass

@router.get("/{id}")
def get_payment(id: str, user_id: str = Depends(require_user)):
    pass