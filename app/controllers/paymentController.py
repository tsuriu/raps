from datetime import datetime, timedelta

import mercadopago
from app.config import settings
from app.controllers.parametersController import get_admin_payment_auth_token

class MP:
    def __init__(self):
        self.platform = "mercado_pago"
        self.sdk = mercadopago.SDK(self.__auth_data__())
        
        
    def __datetime_worker__(self, inicial_date, reserve_time):
        given_time = inicial_date + timedelta(minutes=int(reserve_time))
        final_time = given_time.astimezone().isoformat(timespec="milliseconds")
               
        return final_time
    
    
    def __auth_data__(self):
        return get_admin_payment_auth_token(self.platform)
        
    
    def create_payment(self, build_data):
        payment_data = {
            "transaction_amount": build_data["total_value"],
            "description": build_data["description"],
            "payment_method_id": build_data["payment_method"],
            "payer": {
                "email": build_data["client_email"],
                "first_name": build_data["client_fname"],
                "last_name": build_data["client_lname"]                                
            }
        }
        
        if ("reserve_time" in build_data.keys()) or (build_data["reserve_time"] != 0):
            payment_data["date_of_expiration"] = self.__datetime_worker__(
                                                                build_data["created_at"], 
                                                                build_data["reserve_time"]
                                        )

        if "discount_value" in build_data.keys():
            payment_data["coupon_amount"] = build_data["discount_value"]
        
        payment_response = self.sdk.payment().create(payment_data)
        
        try:
            
            return payment_response["response"]
        except Exception as e:
            return e
        
        
    def get_payment(self, payment_id=None):
        try:
            if payment_id:
                payment_response = self.sdk.payment().get(payment_id=payment_id)
            else:
                payment_response = self.sdk.payment().search()
                
            return payment_response["response"]
        except Exception as e:
            return e
        
        
    def update_payment(self, payment_id, action_type=None, paymant_body=None):
        if action_type == "C":
            paymant_body = {"status": "cancelled"}
        
        try:
            payment_response = self.sdk.payment().update(payment_id, paymant_body)
            return payment_response["response"]
        except Exception as e:
            return e