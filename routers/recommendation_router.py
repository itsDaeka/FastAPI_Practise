# routers/recommendation_router.py

from fastapi import APIRouter, Depends
from services.recommender import RecommenderService
from data.db import get_db
import sqlite3

router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"],
)


def get_recommender(db: sqlite3.Connection = Depends(get_db)) -> RecommenderService:
    return RecommenderService(db)


@router.get(
    "/{user_id}",
    summary="Get a merchant recommendation for a user",
    description="""
Returns the **most frequently visited merchant** for the specified user.

### Logic
- Reads the user's spending history  
- Groups transactions by merchant  
- Selects the merchant with the highest count  
- If user has never spent anywhere → returns `None`  

### Example
```json
{
    "user_id": 1,
    "recommended_merchant_id": 2
}
```

### Responses
- **200 OK** – recommendation computed  
""",
)
def get_recommendations(
    user_id: int,
    recommender: RecommenderService = Depends(get_recommender),
):
    merchant_id = recommender.recommend(user_id)
    return {
        "user_id": user_id,
        "recommended_merchant_id": merchant_id
    }
