from app.database import Purchase
from app.serializers.purchaseSerializers import populatePurchaseEntity


def to_list(number):
    return [int(x) for x in str(number)]


def winner_number(raffle_qtd, lotery):
    zeros = to_list(raffle_qtd).count(0)
    return int("".join(lotery[(zeros * -1):]))


def chk_if_bet(raffle, lotery_num):
    return  True if lotery_num in raffle["selected_bets"] else False


def get_winner(raffle, lotery_num):
    winner_purchase = populatePurchaseEntity(Purchase.find({"slug": raffle["slug"], "selected_bets": lotery_num}))
    return winner_purchase