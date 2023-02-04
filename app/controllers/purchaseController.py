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
    
    return bet


def check_bets(slug: str, user_bet: list):
    raffle = raffleEntity(Raffle.find_one({"slug": slug}))
    
    raffle_selected_bets = raffle["selected_bets"]
    
    used_bets = [ele for ele in user_bet if ele in raffle_selected_bets]
    
    if len(used_bets) != 0:
        return used_bets