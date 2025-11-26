# models/spending_model.py
from pydantic import BaseModel

class SpendingIn(BaseModel):
    user_id: int
    merchant_id: int
    amount: float

class SpendingOut(SpendingIn):
    transaction_id: int
    
class SpendingDeleted(SpendingOut):
    deleted: bool = True