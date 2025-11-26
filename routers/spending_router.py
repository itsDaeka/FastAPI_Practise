# routers/spending_router.py
from typing import List
import sqlite3

from fastapi import APIRouter, Depends
from models.spending_model import SpendingIn, SpendingOut, SpendingDeleted
from data.db import get_db

router = APIRouter(
    prefix="/spendings",
    tags=["spendings"]
)

@router.post("", response_model=SpendingOut)
def create_spending(
    spending: SpendingIn,
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()  # connection represents a database, cursor represents a session for executing queries
    cursor.execute(
        "INSERT INTO spendings (user_id, merchant_id, amount) VALUES (?, ?, ?)",
        (spending.user_id, spending.merchant_id, spending.amount),
    )  # run queries
    db.commit()  # must commit changes if the database has been changed
    new_id = cursor.lastrowid
    
    return SpendingOut(transaction_id=new_id, **spending.model_dump())

@router.delete("/{user_id}", response_model=list[SpendingDeleted])
def delete_spending(
    user_id: int,
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute(
        "SELECT transaction_id, user_id, merchant_id, amount FROM spendings WHERE user_id = ?",
        (user_id,),
    )
    rows = cursor.fetchall()
    cursor.execute(
        "DELETE FROM spendings WHERE user_id = ?",
        (user_id,),
    )
    db.commit()
    
    deletions = [SpendingDeleted(**dict(row)) for row in rows]
    return deletions

@router.get("/{user_id}", response_model=List[SpendingOut])
def get_spendings(
    user_id: int,
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute(
        "SELECT transaction_id, user_id, merchant_id, amount FROM spendings WHERE user_id = ?",
        (user_id,),
    )
    rows = cursor.fetchall()
    
    # rows are sqlite3.Row → convert to dict → Pydantic model
    return [SpendingOut(**dict(row)) for row in rows]
