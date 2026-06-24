from pydantic import BaseModel


'''class PaymentRequest(BaseModel):
    amount: float'''
#newly added to check payment details

class CreatePaymentRequest(BaseModel):
    plan_name: str
    duration_type: str
class VerifyPaymentRequest(BaseModel):

    order_id:str

    transaction_id:str
    gateway_name:str
    payment_success:bool