from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, constr, Field
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
    email: Optional[EmailStr] = Field(None)
    phone: Optional[str] = Field(None)
    password: constr(min_length=8)
    verified: bool = False


class LoginUserSchema(BaseModel):
    email: Optional[EmailStr] = Field(None)
    phone: Optional[str] = Field(None)
    password: constr(min_length=8)


class UserResponseSchema(UserBaseSchema):
    id: str
    pass


class UserResponse(BaseModel):
    status: str
    user: UserBaseSchema


class FilteredUserResponse(UserBaseSchema):
    id: str
    

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
        
        
class RafflePrizeBaseSchema(BaseModel):
    ord_number = str
    prize_description = str
    

class RafflePromotionBaseSchame(BaseModel):
    raffle_qtd = str
    raffle_discount = str
    

class RaffleBaseSchema(BaseModel):
    user: str
    image: str
    title: str
    slug: str
    phone: str
    prize: list 
    promotion: list 
    description: str
    quantity: int
    category: str
    max_buy_quantity: int
    quota_value: float
    expire_reserve: str
    betting_method: str
    selected_bets: Optional[list] = Field([])
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
    image: str | None = None
    description: str | None = None
    phone: str | None = None
    prize: list | None = None
    promotion: list | None = None
    quantity: int | None = None
    category: str | None = None
    max_buy_quantity: int | None = None
    quota_value: float | None = None
    expire_reserve: str | None = None
    betting_method: str | None = None
    selected_bets: list | None = None
    prize_draw_date: str | None = None
    prize_draw_place: str | None = None  
    published: bool | None = None
    published_at: datetime | None = None
    updated_at: datetime | None = None
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
    
        

class CreateRaffleSchema(RaffleBaseSchema):
    user: ObjectId | None = None   

        

class RaffleResponse(RaffleBaseSchema):
    id: str
    user: FilteredUserResponse
    image: str
    title: str
    slug: str
    phone: str
    prize: str
    promotion: str
    description: str
    quantity: int
    category: str
    max_buy_quantity: int
    quota_value: float
    expire_reserve: str
    betting_method: str
    selected_bets: str
    prize_draw_date: str
    prize_draw_place: str
    published: bool = False
    published_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None



class PurchaseBaseSchema(BaseModel):
    raffle: str
    user: str
    quantity: int
    status: Optional[str] = Field(None)
    betting_method: str
    payment_id: Optional[int] = Field(None)
    purchased_at: datetime  | None = None
    bet: Optional[list] = Field([])
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        
        
class PurchaseUpdateSchema(BaseModel):
    raffle: str | None = None
    user: str | None = None
    quantity: int | None = None
    status: str | None = None
    betting_method: str | None = None
    payment_id: int | None = None
    purchased_at: datetime | None = None
    bet: list | None = None
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class CreatePurchaseSchema(PurchaseBaseSchema):
    user: ObjectId | None = None  
    raffle: ObjectId | None = None
    

class PurchaseResponse(PurchaseBaseSchema):
    raffle: str
    user: FilteredUserResponse
    quantity: int
    status: str
    betting_method: str 
    payment_id: int
    purchased_at: datetime
    bet: list
    
class ListPurchaseResponse(BaseModel):
    purchases: List[PurchaseResponse]


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