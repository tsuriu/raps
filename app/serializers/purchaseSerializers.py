from app.serializers.userSerializers import embeddedUserResponse
from app.serializers.raffleSerializers import embeddedRaffleResponse


def purchaseEntity(purchase) -> dict:
    return {
        "id": str(purchase["_id"]),
        "user": str(purchase["user"]),
        "raffle": str(purchase["raffle"]),
        "quantity": purchase["quantity"],
        "status": purchase["status"],
        "purchased_at": purchase["purchased_at"],
        "bet": purchase["bet"]
    }

def populatePurchaseEntity(purchase) -> dict:
    return {
        "id": str(purchase["_id"]),
        "user": embeddedUserResponse(purchase["user"]),
        "raffle": embeddedRaffleResponse(purchase["raffle"]),
        "quantity": purchase["quantity"],
        "status": purchase["status"],
        "purchased_at": purchase["purchased_at"],
        "bet": purchase["bet"]
    }

def embeddedPurchaseResponse(purchase) -> dict:
    return {
        "id": str(purchase["_id"]),
        "user": embeddedUserResponse(purchase["user"]),
        "raffle": embeddedRaffleResponse(purchase["raffle"]),
        "quantity": purchase["quantity"],
        "status": purchase["status"],
        "purchased_at": purchase["purchased_at"],
        "bet": purchase["bet"]
    }

def purchaseResponseEntity(purchase) -> dict:
    return {}

def purchaseListEntity(purchases) -> list:
    return [purchaseEntity(purchase) for purchase in purchases]