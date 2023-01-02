from app.serializers.userSerializers import embeddedUserResponse

def eventEntity(event) -> dict:
    return {
        "id": str(event["_id"]),
        "owner_id": str(event["owner_id"]),
        "description": event["description"],
        "quantity": event["quantity"],
        "category": event["category"],
        "max_buy_quantity": event["max_buy_quantity"],
        "quota_value": event["quota_value"],
        "expire_reserve": event[" expire_reserve"],
        "prize_draw_date": event["prize_draw_date"],
        "prize_draw_place": event["prize_draw_place"],
        "published": event["published"],
        "created_at": event["created_at"],
        "updated_at": event["updated_at"]    
    }

def populateEventEntity(event) -> dict:
    return {
        "id": str(event["_id"]),
        "owner_id": embeddedUserResponse(event["owner_id"]),
        "description": event["description"],
        "quantity": event["quantity"],
        "category": event["category"],
        "max_buy_quantity": event["max_buy_quantity"],
        "quota_value": event["quota_value"],
        "expire_reserve": event[" expire_reserve"],
        "prize_draw_date": event["prize_draw_date"],
        "prize_draw_place": event["prize_draw_place"],
        "published": event["published"],
        "published_at": event["published_at"],
        "created_at": event["created_at"],
        "updated_at": event["updated_at"]    
    }
    
def embeddedEventResponse(event) -> dict:
    return {
        "id": str(event["_id"]),
        "owner_id": embeddedUserResponse(event["owner_id"]),
        "description": event["description"],
        "quantity": event["quantity"],
        "category": event["category"],
        "max_buy_quantity": event["max_buy_quantity"],
        "quota_value": event["quota_value"],
        "expire_reserve": event[" expire_reserve"],
        "prize_draw_date": event["prize_draw_date"],
        "prize_draw_place": event["prize_draw_place"],
        "published": event["published"],
        "created_at": event["created_at"]                         
    }

def eventListEntity(events) -> list:
    return [eventEntity(event) for event in events]