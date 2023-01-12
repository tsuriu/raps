from fastapi import APIRouter, Depends, HTTPException, status, Response
from pymongo.collection import ReturnDocument

from bson.objectid import ObjectId
from app.serializers.userSerializers import userResponseEntity, userEntity, userListEntity

from app.database import User
from .. import schemas, oauth2

from app.oauth2 import require_user


router = APIRouter()


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: str, user_id: str = Depends(oauth2.require_user)):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {user_id}")
        
    if id == "me":
        user = userResponseEntity(User.find_one({'_id': ObjectId(str(user_id))}))
    else:
        user = userResponseEntity(User.find_one({'_id': ObjectId(str(id))}))        
        
    
    return {"status": "success", "user": user}


@router.get("/")
def get_users(limit: int = 10, page: int = 1, user_id: str = Depends(require_user)):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {user_id}")
        
    skip = (page - 1) * limit
    pipeline = [
        {'$match': {}},
        {
            '$skip': skip
        }, {
            '$limit': limit
        }
    ]
    
    users = userListEntity(User.aggregate(pipeline))
    return {'status': 'success', 'results': len(users), 'users':users}


@router.put("/{id}")
def update_me(id: str, payload: schemas.UserUpdateSchema, user_id: str = Depends(require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
    updated_user = User.find_one_and_update(
        {'_id': ObjectId(id)}, {'$set': payload.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No user with this id: {id} found')
        
    return userEntity(updated_user)

@router.delete("/{id}")
def delete_user(id: str, user_id: str = Depends(require_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
    user = User.find_one_and_delete({'_id': ObjectId(id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No user with this id: {id} found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)
