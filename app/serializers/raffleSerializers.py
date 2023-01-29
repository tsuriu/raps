from app.serializers.userSerializers import embeddedUserResponse, embeddedUserResponse_NoAuth

def prizeEntity(prize) -> dict:
    return {
        "ord_number": prize["ord_number"],
        "prize_description": str(prize["prize_description"])
    }
    
def promotionEntity(promotion) -> dict:
    return {
        "raffle_qtd": promotion["raffle_qtd"],
        "raffle_discount": promotion["raffle_discount"]
    }


def raffleEntity(raffle) -> dict:
    return {
        "id": str(raffle["_id"]),
        "user": embeddedUserResponse(raffle["user"]),
        "title": raffle["title"],
        "slug": raffle["slug"],
        "phone": raffle["phone"],
        "prize": raffle["prize"], #prizeEntity(raffle["prize"]),
        "promotion": raffle["promotion"], #promotionEntity(raffle["promotion"]), 
        "description": str(raffle["description"]),
        "quantity": raffle["quantity"],
        "category": raffle["category"],
        "max_buy_quantity": raffle["max_buy_quantity"],
        "quota_value": raffle["quota_value"],
        "expire_reserve": raffle["expire_reserve"],
        "betting_method": raffle["betting_method"],
        "selected_bets": raffle["selected_bets"],
        "prize_draw_date": raffle["prize_draw_date"],
        "prize_draw_place": raffle["prize_draw_place"],
        "published": raffle["published"],
        "created_at": raffle["created_at"],
        "updated_at": raffle["updated_at"]    
    }

def populateRaffleEntity(raffle) -> dict:
    return {
        "id": str(raffle["_id"]),
        "user": embeddedUserResponse(raffle["user"]),
        "title": raffle["title"],
        "slug": raffle["slug"],
        "phone": raffle["phone"],
        "prize": raffle["prize"], #prizeEntity,
        "promotion": raffle["promotion"], #promotionEntity, 
        "description": str(raffle["description"]),
        "quantity": raffle["quantity"],
        "category": raffle["category"],
        "max_buy_quantity": raffle["max_buy_quantity"],
        "quota_value": raffle["quota_value"],
        "expire_reserve": raffle["expire_reserve"],
        "betting_method": raffle["betting_method"],
        "selected_bets": raffle["selected_bets"],
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
        "user": embeddedUserResponse(raffle["user"]),
        "title": raffle["title"],
        "slug": raffle["slug"],
        "phone": raffle["phone"],
        "prize": raffle["prize"], #prizeEntity,
        "promotion": raffle["promotion"], # promotionEntity, 
        "description": str(raffle["description"]),
        "quantity": raffle["quantity"],
        "category": raffle["category"],
        "max_buy_quantity": raffle["max_buy_quantity"],
        "quota_value": raffle["quota_value"],
        "expire_reserve": raffle["expire_reserve"],
        "betting_method": raffle["betting_method"],
        "selected_bets": raffle["selected_bets"],
        "prize_draw_date": raffle["prize_draw_date"],
        "prize_draw_place": raffle["prize_draw_place"],
        "published": raffle["published"],
        "created_at": raffle["created_at"]                         
    }
    
def raffleResponseEntity(raffle) -> dict:
    return {
        "user": embeddedUserResponse_NoAuth(raffle["user"]),
        "title": raffle["title"],
        "slug": raffle["slug"],
        "phone": raffle["phone"],
        "prize": raffle["prize"], #prizeEntity,
        "promotion": raffle["promotion"], #promotionEntity,
        "description": str(raffle["description"]),
        "quantity": raffle["quantity"],
        "category": raffle["category"],
        "max_buy_quantity": raffle["max_buy_quantity"],
        "quota_value": raffle["quota_value"],
        "expire_reserve": raffle["expire_reserve"],
        "betting_method": raffle["betting_method"],
        "selected_bets": raffle["selected_bets"],
        "prize_draw_date": raffle["prize_draw_date"],
        "prize_draw_place": raffle["prize_draw_place"],
        "published": raffle["published"],
        "created_at": raffle["created_at"],
    }

def raffleListEntity(raffles) -> list:
    return [populateRaffleEntity(raffle) for raffle in raffles]


def raffleListEntity_NoAuth(raffles) -> list:
    return [raffleResponseEntity(raffle) for raffle in raffles]