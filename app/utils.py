from passlib.context import CryptContext
import random as rand

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def auto_bet(sorted_numbers: list, max_quotas: int, samples: int):
    quotas = list(range(max_quotas))
    
    if len(sorted_numbers) > 0:
        for num in sorted_numbers:
            quotas.remove(num)
            
    bet = rand.sample(quotas, samples)
    
    return bet