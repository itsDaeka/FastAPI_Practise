# routers/matrix_router.py

from fastapi import APIRouter, Depends
import sqlite3
from data.db import get_db

router = APIRouter(
    tags=["matrix"]
)

@router.get(
    "/matrix_properties",
    summary="Get the shape of the user–merchant matrix",
    description="""
Returns information about the implicit **user × merchant** spending matrix.

### Logic
- Counts distinct users  
- Counts distinct merchants  
- Returns the matrix dimension (`rows × columns`)  

### Responses
- **200 OK** – matrix dimension returned successfully  
""",
)
def matrix_properties(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()

    users_nb = cursor.execute(
        "SELECT COUNT(DISTINCT user_id) FROM spendings"
    ).fetchone()[0]

    merchants_nb = cursor.execute(
        "SELECT COUNT(DISTINCT merchant_id) FROM spendings"
    ).fetchone()[0]

    return {
        "rows": users_nb,
        "cols": merchants_nb,
        "note": "Rows = users, Columns = merchants"
    }
