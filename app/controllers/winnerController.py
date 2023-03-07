from app.database import Purchase, User

from bson.objectid import ObjectId

from app.serializers.purchaseSerializers import purchaseEntity
from app.serializers.userSerializers import embeddedUserResponse_NoAuth

def to_list(number):
    return [int(x) for x in str(number)]


def winner_number(raffle_qtd, lotery):
    zeros = to_list(raffle_qtd).count(0)
    lotery = [str(x) for x in to_list(lotery)]
    return int("".join(lotery[(zeros * -1):]))


def chk_if_bet(raffle, lotery_num):
    return  True if lotery_num in raffle["selected_bets"] else False


def get_winner_purchase(slug, lotery_num):
    winner_purchase = purchaseEntity(Purchase.find_one({"raffle": slug, "bet": lotery_num}))
    user = embeddedUserResponse_NoAuth(User.find_one({"_id": ObjectId(winner_purchase["user"])}))
        
    winner_purchase["user"] = user
    return winner_purchase