import base64
from typing import List
from fastapi import Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from bson.objectid import ObjectId

from app.serializers.userSerializers import userEntity
from app.controllers.parametersController import get_auth_params

from .database import User
from .schemas import UserBaseSchema
from .config import settings

auth_params = get_auth_params()

class Settings(BaseModel):
    authjwt_algorithm: str = auth_params["jwt_algorithm"]
    authjwt_decode_algorithms: List[str] = [auth_params["jwt_algorithm"]]
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access","refresh"}
    authjwt_token_location: set = {'cookies', 'headers'}
    authjwt_access_cookie_key: str = 'access_token'
    authjwt_refresh_cookie_key: str = 'refresh_token'
    authjwt_cookie_csrf_protect: bool = False
    authjwt_public_key: str = base64.b64decode(
        settings.JWT_PUBLIC_KEY).decode('utf-8')
    authjwt_private_key: str = base64.b64decode(
        settings.JWT_PRIVATE_KEY).decode('utf-8')


denylist = set()


@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in denylist

@AuthJWT.load_config
def get_config():
    return Settings()


class NotVerified(Exception):
    pass


class UserNotFound(Exception):
    pass


def require_user(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        user_id = Authorize.get_jwt_subject()
        user = userEntity(User.find_one({'_id': ObjectId(str(user_id))}))

        if not user:
            raise UserNotFound('User no longer exist')

        if not user["verified"]:
            raise NotVerified('You are not verified')

    except Exception as e:
        error = e.__class__.__name__
        print(error)
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not logged in')
        if error == 'UserNotFound':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='User no longer exist')
        if error == 'NotVerified':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Please verify your account')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid or has expired')
    return user_id


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user_id: str = Depends(require_user)):
        user = userEntity(User.find_one({"_id": ObjectId(user_id)}))
    
        if user["role"] not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Operation not permitted")