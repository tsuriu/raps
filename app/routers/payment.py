import json

from fastapi import APIRouter, Depends, HTTPException, status, Response

from pymongo.collection import ReturnDocument

from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError

router = APIRouter()

@router.post("/mp")
def mp_hook():
    pass
