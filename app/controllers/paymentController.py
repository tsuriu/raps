from datetime import datetime, timedelta

import mercadopago
from app.config import settings

class MP:
    def __init__(self):
        self.mp_token = settings.MP_TOKEN
        self.sdk = mercadopago.SDK(self.mp_token)
        
        
    def __datetime_worker__(self, inicial_date, reserve_time):
        date_format_str = '%Y-%m-%dT%H:%M:%S.%fZ'
        
        given_time = datetime.strptime(inicial_date, date_format_str)
        final_time = given_time + timedelta(minutes=reserve_time)
               
        return final_time.strftime(date_format_str)
    
    
    def create_payment(self, build_data):
        payment_data = {
            "transaction_amount": build_data["total_value"],
            "description": build_data["description"],
            "payment_method_id": build_data["payment_method"],
            "payer": {
                "email": build_data["client_email"],
                "first_name": build_data["client_fname"],
                "last_name": build_data["client_lname"]                                
            },
            "date_of_expiration": "2022-11-17T09:37:52.000-04:00"
        }
        
        if "reserve_time" in build_data.keys():
            payment_data["date_of_expiration"] = self.__datetime_worker__(
                                                                build_data["created_at"], 
                                                                build_data["reserve_times"]
                                        )

        if "discount_value" in build_data.keys():
            payment_data["coupon_amount"] = build_data["discount_value"]
        
        try:
            payment_response = self.sdk.payment().create(payment_data)
            return payment_response["response"]
        except Exception as e:
            return e
        
        
    def get_payment(self, payment_id=None):
        try:
            payment_response = self.sdk.payment().get(payment_id=payment_id)
            return payment_response["response"]
        except Exception as e:
            return e
        
        
    def cancel_payment(self, payment_id):
        payment_data = {"status": "cancelled"}
        
        try:
            payment_response = self.sdk.payment().update(payment_id, payment_data)
            return payment_response["response"]
        except Exception as e:
            return e