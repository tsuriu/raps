from app.serializers.userSerializers import embeddedUserResponse

def raffleEntity(raffle) -> dict:
    return {
        "id": str(raffle["_id"]),
        "owner_id": str(raffle["owner_id"]),
        "description": raffle["description"],
        "quantity": raffle["quantity"],
        "category": raffle["category"],
        "max_buy_quantity": raffle["max_buy_quantity"],
        "quota_value": raffle["quota_value"],
        "expire_reserve": raffle[" expire_reserve"],
        "prize_draw_date": raffle["prize_draw_date"],
        "prize_draw_place": raffle["prize_draw_place"],
        "published": raffle["published"],
        "created_at": raffle["created_at"],
        "updated_at": raffle["updated_at"]    
    }

def populateRaffleEntity(raffle) -> dict:
    return {
        "id": str(raffle["_id"]),
        "owner_id": embeddedUserResponse(raffle["owner_id"]),
        "description": raffle["description"],
        "quantity": raffle["quantity"],
        "category": raffle["category"],
        "max_buy_quantity": raffle["max_buy_quantity"],
        "quota_value": raffle["quota_value"],
        "expire_reserve": raffle[" expire_reserve"],
        "prize_draw_date": raffle["prize_draw_date"],
        "prize_draw_place": raffle["prize_draw_place"],
        "published": raffle["published"],
        "published_at": raffle["published_at"],
        "created_at": raffle["created_at"],
        "updated_at": raffle["updated_at"]    
    }
    
def embeddedRaffleResponse(raffle) -> dict:
    return {
        "id": str(raffle["_id"]),
        "owner_id": embeddedUserResponse(raffle["owner_id"]),
        "description": raffle["description"],
        "quantity": raffle["quantity"],
        "category": raffle["category"],
        "max_buy_quantity": raffle["max_buy_quantity"],
        "quota_value": raffle["quota_value"],
        "expire_reserve": raffle[" expire_reserve"],
        "prize_draw_date": raffle["prize_draw_date"],
        "prize_draw_place": raffle["prize_draw_place"],
        "published": raffle["published"],
        "created_at": raffle["created_at"]                         
    }

def raffleListEntity(raffles) -> list:
    return [raffleEntity(raffle) for raffle in raffles]