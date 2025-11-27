from pydantic import BaseModel

class SpendingIn(BaseModel):
    user_id: int
    merchant_id: int
    amount: float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": 1,
                    "merchant_id": 2,
                    "amount": 19.99
                },
                {
                    "user_id": 5,
                    "merchant_id": 1,
                    "amount": 5.75
                }
            ]
        }
    }

class SpendingOut(BaseModel):
    transaction_id: int
    user_id: int
    merchant_id: int
    amount: float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "transaction_id": 101,
                    "user_id": 1,
                    "merchant_id": 2,
                    "amount": 19.99
                }
            ]
        }
    }

class SpendingDeleted(BaseModel):
    transaction_id: int
    user_id: int
    merchant_id: int
    amount: float
    deleted: bool

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "transaction_id": 101,
                    "user_id": 1,
                    "merchant_id": 2,
                    "amount": 19.99,
                    "deleted": True
                }
            ]
        }
    }