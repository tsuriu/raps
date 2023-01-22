import random as rand

from app.serializers.raffleSerializers import raffleEntity

from app import schemas
from app.database import Raffle



def auto_bet(sorted_numbers: list, max_quotas: int, samples: int):
    quotas = list(range(max_quotas))
    
    if len(sorted_numbers) > 0:
        for num in [int(x) for x in sorted_numbers]:
            quotas.remove(num)
            
    bet = rand.sample(quotas, samples)
    
    return ",".join(str(v) for v in bet)


def check_bets(raffle_id: str, bet: str):
    raffle = raffleEntity(Raffle.find_one({"_id": raffle_id}))
    
    raffle_selected_bets = raffle["selected_bets"].split(",")
    user_bet = bet.split(",")
    
    if not any(ele in raffle_selected_bets for ele in user_bet):
        return True
    else:
        return False