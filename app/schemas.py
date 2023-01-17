from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr, constr
from bson.objectid import ObjectId


class UserBaseSchema(BaseModel):
    name: str
    email: str
    phone: str
    role: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    role: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class CreateUserSchema(UserBaseSchema):
    password: constr(min_length=8)
    verified: bool = False


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class UserResponseSchema(UserBaseSchema):
    id: str
    pass


class UserResponse(BaseModel):
    status: str
    user: UserResponseSchema


class FilteredUserResponse(UserBaseSchema):
    id: str
    
########################################################################################
class SessionBaseSchema(BaseModel):
    id: str
    user: str
    created_at: datetime | None = None
    refreshed_at: datetime | None = None

    class Config:
        orm_mode = True

class SessionResponse(BaseModel):
    id: str
    user: FilteredUserResponse
    created_at: datetime | None = None
    refreshed_at: datetime | None = None

    class Config:
        orm_mode = True    
    
########################################################################################
    
    
class RaffleBaseSchema(BaseModel):
    user: str
    title: str
    description: str
    quantity: int
    category: str
    max_buy_quantity: int
    quota_value: float
    expire_reserve: str
    prize_draw_date: str
    prize_draw_place: str
    published: bool = False
    published_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        
        
class RaffleUpdateSchema(BaseModel):
    user: str | None = None
    description: str | None = None
    quantity: int | None = None
    category: str | None = None
    max_buy_quantity: int | None = None
    quota_value: float | None = None
    expire_reserve: str | None = None
    prize_draw_date: str | None = None
    prize_draw_place: str | None = None  
    published: bool | None = None
    updated_at: datetime | None = None
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
    
        

class CreateRaffleSchema(RaffleBaseSchema):
    user: ObjectId | None = None   

class RaffleBoughtQuota(BaseModel):
    raffle_id: int
    bought_quantity: int
    bought_value: float
    is_resevertion: bool = False
    buyer_name: str
    buyer_phne: str
    purchased_at: datetime | None = None
        
    class Config:
        orm_mode = True
        

class RaffleResponse(RaffleBaseSchema):
    id: str
    user: FilteredUserResponse
    title: str
    description: str
    quantity: int
    category: str
    max_buy_quantity: int
    quota_value: float
    expire_reserve: str
    prize_draw_date: str
    prize_draw_place: str
    published: bool = False
    published_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


########################################################################################


class PostBaseSchema(BaseModel):
    title: str
    content: str
    category: str
    image: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class CreatePostSchema(PostBaseSchema):
    user: ObjectId | None = None
    pass


class PostResponse(PostBaseSchema):
    id: str
    user: FilteredUserResponse
    created_at: datetime
    updated_at: datetime


class UpdatePostSchema(BaseModel):
    title: str | None = None
    content: str | None = None
    category: str | None = None
    image: str | None = None
    user: str | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ListPostResponse(BaseModel):
    status: str
    results: int
    posts: List[PostResponse]