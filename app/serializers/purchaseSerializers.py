from app.serializers.userSerializers import embeddedUserResponse, userResponseEntity
from app.serializers.raffleSerializers import embeddedRaffleResponse


def purchaseEntity(purchase) -> dict:
    return {
        "id": str(purchase["_id"]),
        "user": str(purchase["user"]),
        "raffle": str(purchase["raffle"]),
        "quantity": purchase["quantity"],
        "status": purchase["status"],
        "payment_id": purchase["payment_id"],
        "betting_method": purchase["betting_method"],
        "purchased_at": purchase["purchased_at"],
        "bet": purchase["bet"]
    }

def populatePurchaseEntity(purchase) -> dict:
    return {
        "id": str(purchase["_id"]),
        "user": embeddedUserResponse(purchase["user"]),
        "raffle": str(purchase["raffle"]),
        "quantity": purchase["quantity"],
        "status": purchase["status"],
        "betting_method": purchase["betting_method"],
        "payment_id": purchase["payment_id"],
        "purchased_at": purchase["purchased_at"],
        "bet": purchase["bet"]
    }

def embeddedPurchaseResponse(purchase) -> dict:
    return {
        "id": str(purchase["_id"]),
        "user": embeddedUserResponse(purchase["user"]),
        "raffle": str(purchase["raffle"]),
        "quantity": purchase["quantity"],
        "status": purchase["status"],
        "betting_method": purchase["betting_method"],
        "payment_id": purchase["payment_id"],
        "purchased_at": purchase["purchased_at"],
        "bet": purchase["bet"]
    }

def purchaseResponseEntity(purchase) -> dict:
    return {
        "user": embeddedUserResponse(purchase["user"]),
        "raffle": embeddedRaffleResponse(purchase["raffle"]),
        "quantity": purchase["quantity"],
        "status": purchase["status"],
        "betting_method": purchase["betting_method"],
        "payment_id": purchase["payment_id"],
        "purchased_at": purchase["purchased_at"],
        "bet": purchase["bet"]
    }

def purchaseListEntity(purchases) -> list:
    return [embeddedPurchaseResponse(purchase) for purchase in purchases]