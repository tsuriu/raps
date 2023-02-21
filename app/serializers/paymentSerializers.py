def paymentEntity(payment) -> dict:
    return {
        "id": payment["id"],
        "status": payment["status"],
        "status_detail": payment["status_detail"],
        "description": payment["description"],
        "payment_type_id": payment["payment_type_id"],
        "date_created": payment["date_created"],
        "date_approved": payment["date_approved"],
        "transaction_amount": payment["transaction_amount"],
        "transaction_amount_refunded": payment["transaction_amount_refunded"],
        "coupon_amount": payment["coupon_amount"],
        "payer": payment["payer"]
    }
    
def paymentListEntity(purchases) -> list:
    return [paymentEntity(purchase) for purchase in purchases]