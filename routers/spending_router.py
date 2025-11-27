# routers/spending_router.py

from fastapi import APIRouter, Depends, Body
import sqlite3
from models.spending_model import SpendingIn, SpendingOut, SpendingDeleted
from data.db import get_db

router = APIRouter(
    prefix="/spendings",
    tags=["spendings"]
)

# Request examples for POST /spendings
spending_examples = {
    "normal": {
        "summary": "A normal spending entry",
        "description": "A valid spending record with user, merchant, and amount.",
        "value": {
            "user_id": 1,
            "merchant_id": 2,
            "amount": 19.99
        },
    },
    "converted_amount": {
        "summary": "FastAPI auto-converts amount strings",
        "description": "Shows how FastAPI converts string numbers to floats.",
        "value": {
            "user_id": 1,
            "merchant_id": 2,
            "amount": "19.99"
        },
    },
    "invalid_amount": {
        "summary": "Invalid amount produces validation error",
        "value": {
            "user_id": 1,
            "merchant_id": 2,
            "amount": "nineteen"
        },
    },
}


@router.post(
    "",
    summary="Create a spending entry",
    description="""
Creates a new spending entry in the SQLite database.

### Workflow
- Validates the incoming spending object  
- Inserts a new record into the `spendings` table  
- Returns the inserted row as a `SpendingOut` object  

### Responses
- **200 OK** – spending entry created successfully  
""",
    response_model=SpendingOut,
)
def create_spending(
    spending: SpendingIn = Body(..., openapi_examples=spending_examples),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO spendings (user_id, merchant_id, amount) VALUES (?, ?, ?)",
        (spending.user_id, spending.merchant_id, spending.amount),
    )
    db.commit()
    transaction_id = cursor.lastrowid
    return SpendingOut(
        transaction_id=transaction_id,
        user_id=spending.user_id,
        merchant_id=spending.merchant_id,
        amount=spending.amount,
    )


@router.get(
    "/{user_id}",
    summary="Get all spendings for a user",
    description="""
Returns all spending entries associated with a given `user_id`.

### Workflow
- Queries the database for all transactions belonging to the user  
- Returns them as a list of `SpendingOut` objects  

### Responses
- **200 OK** – list of spendings (possibly empty)
""",
)
def get_spendings(
    user_id: int,
    db: sqlite3.Connection = Depends(get_db),
):
    cursor = db.cursor()
    rows = cursor.execute(
        "SELECT transaction_id, user_id, merchant_id, amount FROM spendings WHERE user_id = ?",
        (user_id,),
    ).fetchall()

    return [SpendingOut(**dict(row)) for row in rows]


@router.delete(
    "/{user_id}",
    summary="Delete all spendings for a user",
    description="""
Deletes every spending entry belonging to the specified user.

### Workflow
- Fetches all spendings first  
- Deletes matching rows  
- Returns all deleted entries wrapped in `SpendingDeleted`  

### Responses
- **200 OK** – deleted entries returned
""",
    response_model=list[SpendingDeleted],
)
def delete_spendings(
    user_id: int,
    db: sqlite3.Connection = Depends(get_db),
):
    cursor = db.cursor()

    # Fetch existing spendings
    rows = cursor.execute(
        "SELECT transaction_id, user_id, merchant_id, amount FROM spendings WHERE user_id = ?",
        (user_id,),
    ).fetchall()

    # Delete them
    cursor.execute("DELETE FROM spendings WHERE user_id = ?", (user_id,))
    db.commit()

    return [
        SpendingDeleted(
            transaction_id=row["transaction_id"],
            user_id=row["user_id"],
            merchant_id=row["merchant_id"],
            amount=row["amount"],
            deleted=True,
        )
        for row in rows
    ]
