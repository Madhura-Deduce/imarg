from pydantic import BaseModel


'''class PaymentRequest(BaseModel):
    amount: float'''
#newly added to check payment details

class CreatePaymentRequest(BaseModel):
    plan_name: str
    duration_type: str
    #amount:float
class VerifyPaymentRequest(BaseModel):

    order_id:str

    transaction_id:str
    gateway_name:str
    payment_success:bool
    #transaction_id: str
    #payment_gateway: str = "MANUAL"
    