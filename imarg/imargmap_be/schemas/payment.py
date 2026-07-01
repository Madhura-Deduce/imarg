from pydantic import BaseModel



class CreatePaymentRequest(BaseModel):
    plan_name: str
    duration_type: str
class VerifyPaymentRequest(BaseModel):

    order_id:str

    transaction_id:str
    gateway_name:str
    payment_success:bool
    #transaction_id: str
    #payment_gateway: str = "MANUAL"