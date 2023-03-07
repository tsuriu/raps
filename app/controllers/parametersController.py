from app.database import Parameters
from app.config import settings

def get_raffle_taxes():
    return Parameters.find_one({"config_description":"raffle_publishment_taxes"})


def calc_raffle_taxes(raffle):
    taxes = get_raffle_taxes()["data"]
    raffleTotalValue = raffle["quantity"] * raffle["quota_value"]
    publishRate = 0
    
    for idx, tax in enumerate(taxes):
        if idx != len(taxes) + 1:
            if tax["billingRate"] <= raffleTotalValue < taxes[idx + 1]["billingRate"]:
                publishRate = tax["rate"]
        else:
            publishRate = taxes[len(taxes) + 1]["rate"]
            
    return publishRate, raffleTotalValue


def get_admin_payment_auth_token(platform):
    auth_data = Parameters.find_one({"config_description":"admin_payments"})
    auth = [dt for dt in auth_data["data"] if dt["channel_name"] == platform][0]
        
    if settings.DEVENV:
        return auth["dev_token"]
    else:
        return auth["prd_token"]


def get_auth_params():
    auth_params = Parameters.find_one({"config_description":"auth_config_elements"})
    
    return auth_params["data"]