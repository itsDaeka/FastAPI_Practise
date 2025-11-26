# routers/matrix_router.py
from fastapi import APIRouter, Depends
import sqlite3
from data.db import get_db

router = APIRouter(
    tags=["matrix"]
)

@router.get("/matrix_properties")
def get_matrix(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(DISTINCT user_id) as users FROM spendings")
    row_users = cursor.fetchone()
    users_nb = row_users["users"] if row_users else 0

    cursor.execute("SELECT COUNT(DISTINCT merchant_id) as merchants FROM spendings")
    row_merchants = cursor.fetchone()
    merchants_nb = row_merchants["merchants"] if row_merchants else 0
    
    return {
        "rows": users_nb, 
        "cols": merchants_nb,
        "note": "Number of rows correspond to number of users, and columns correspond to number of merchants."
    }
