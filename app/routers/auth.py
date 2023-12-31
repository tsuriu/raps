from datetime import datetime, timedelta
import hashlib
from random import randbytes
from bson.objectid import ObjectId
from fastapi import APIRouter, Request, Response, status, Depends, HTTPException
from pydantic import EmailStr

from app import oauth2
from app.database import User
from app.email import Email
from app.serializers.userSerializers import userEntity, userResponseEntity
from app.controllers.parametersController import get_auth_params

from .. import schemas, utils
from app.oauth2 import AuthJWT, denylist
from ..config import settings

auth_params = get_auth_params()

router = APIRouter()
ACCESS_TOKEN_EXPIRES_IN = auth_params["access_token_expires_in"]
REFRESH_TOKEN_EXPIRES_IN = auth_params["refresh_token_expires_in"]
VERIFICATION_BASE_URL = auth_params["verification_base_url"]


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def create_user(payload: schemas.CreateUserSchema, request: Request):        
    check_dup = {}
    
    if payload.email:
        check_dup = {'email': payload.email.lower()}
        payload.role = 'user'
        payload.email = payload.email.lower()
        #  Hash the password
        payload.password = utils.hash_password(payload.password)

    
    if payload.phone and not payload.email:
        check_dup = {'phone': payload.phone}
        
        payload.role = 'cli'
        payload.verified = True
        payload.email = "{}@cli.rifatu".format(payload.phone)
        #  Hash the password
        payload.password = utils.hash_password(payload.phone)

    
    # Check if user already exist
    user = User.find_one(check_dup)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Account already exist')
    
    #HML
    payload.created_at = datetime.utcnow()
    payload.updated_at = payload.created_at

    result = User.insert_one(payload.dict())
    new_user = User.find_one({'_id': result.inserted_id})
    try:
        token = randbytes(10)
        hashedCode = hashlib.sha256()
        hashedCode.update(token)
        verification_code = hashedCode.hexdigest()
        User.find_one_and_update({"_id": result.inserted_id}, {
            "$set": {"verification_code": verification_code, "updated_at": datetime.utcnow()}})

        if VERIFICATION_BASE_URL:
            verification_base_url = VERIFICATION_BASE_URL
        else:
            verification_base_url = f"{request.url.scheme}://{request.client.host}:{request.url.port}"
            
        url = f"{verification_base_url}/api/auth/verifyemail/{token.hex()}"
        #await Email(userEntity(new_user), url, [EmailStr(payload.email)]).sendVerificationCode()
    except Exception as error:
        User.find_one_and_update({"_id": result.inserted_id}, {
            "$set": {"verification_code": None, "updated_at": datetime.utcnow()}})
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='There was an error sending email')
    
    if settings.DEVENV:
        return {'status': 'success', 'verify_link': url, 'message': 'Verification token successfully sent to your email'}
    else:
        return {'status': 'success', 'message': 'Verification token successfully sent to your email'}


@router.post('/login')
def login(payload: schemas.LoginUserSchema, response: Response, Authorize: AuthJWT = Depends()):
    # Check if the user exist
    db_user = User.find_one({'email': payload.email.lower()})
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')
    user = userEntity(db_user)

    # Check if user verified his email
    if not user['verified']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Please verify your email address')

    # Check if the password is valid
    if not utils.verify_password(payload.password, user['password']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')

    # Create access token
    access_token = Authorize.create_access_token(
        subject=str(user["id"]), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

    # Create refresh token
    refresh_token = Authorize.create_refresh_token(
        subject=str(user["id"]), expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN))

    # Store refresh and access tokens in cookie
    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('refresh_token', refresh_token,
                        REFRESH_TOKEN_EXPIRES_IN * 60, REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')

    # Send both access
    return {'status': 'success', 'access_token': access_token, 'user': userResponseEntity(db_user)}


@router.get('/refresh')
def refresh_token(response: Response, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()

        user_id = Authorize.get_jwt_subject()
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not refresh access token')
        user = userEntity(User.find_one({'_id': ObjectId(str(user_id))}))
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='The user belonging to this token no logger exist')
            
        
        jti = Authorize.get_raw_jwt()
        denylist.add(jti['jti'])
        
        access_token = Authorize.create_access_token(
            subject=str(user["id"]), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Please provide refresh token')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')
    return {'access_token': access_token}


@router.get('/logout', status_code=status.HTTP_200_OK)
def logout(response: Response, Authorize: AuthJWT = Depends(), user_id: str = Depends(oauth2.require_user)):
    jti = Authorize.get_raw_jwt()
    denylist.add(jti['jti'])
    
    Authorize.unset_jwt_cookies()
    response.set_cookie('logged_in', '', -1)

    return {'status': 'success'}


@router.get('/verifyemail/{token}')
def verify_me(token: str):
    hashedCode = hashlib.sha256()
    hashedCode.update(bytes.fromhex(token))
    verification_code = hashedCode.hexdigest()
    result = User.find_one_and_update({"verification_code": verification_code}, {
        "$set": {"verification_code": None, "verified": True, "updated_at": datetime.utcnow()}}, new=True)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid verification code or account already verified')
    return {
        "status": "success",
        "message": "Account verified successfully"
    }
