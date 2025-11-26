# routers/recommendation_router.py
from fastapi import APIRouter, Depends
import sqlite3
from data.db import get_db
from services.recommender import RecommenderService

router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"]
)

def get_recommender(db: sqlite3.Connection = Depends(get_db)) -> RecommenderService:
    return RecommenderService(db)

@router.get("/{user_id}")
def get_recommendations(
    user_id: int,
    recommender: RecommenderService = Depends(get_recommender)
):
    merchant_id = recommender.recommend(user_id)
    return {
        "user_id": user_id,
        "recommended_merchant_id": merchant_id
    }



# from fastapi import APIRouter, Depends
# import sqlite3
# from data.db import get_db

# RECOMENDATION_QUERY = """
# SELECT merchant_id
# FROM (
#     SELECT user_id, merchant_id, COUNT(*) AS transaction_count
#     FROM spendings s
#     GROUP BY user_id, merchant_id
#     HAVING COUNT(*) = (
#         SELECT COUNT(*)
#         FROM spendings s2
#         WHERE s2.user_id = s.user_id
#         GROUP BY merchant_id
#         ORDER BY COUNT(*) DESC
#         LIMIT 1
#     )
# )
# WHERE user_id = ?;
# """

# router = APIRouter(
#     prefix="/recommendations",
#     tags=["recommendations"]
# )

# @router.get("/{user_id}")
# def get_recommendations(
#     user_id: int,
#     db: sqlite3.Connection = Depends(get_db)
# ):
#     cursor = db.cursor()
#     cursor.execute(
#         RECOMENDATION_QUERY,
#         (user_id,)
#     )
#     row = cursor.fetchone()
#     print(row["merchant_id"] if row else "No data found")
#     return {
#         "user_id": user_id,
#         "recommended_merchant_id": row["merchant_id"] if row else None
#     }
#     # if row is None or row["cnt"] == 0:
#     #     return {"user_id": user_id, "recommendations": []}

#     # return {
#     #     "user_id": user_id,
#     #     "recommendations": ["Store A", "Store B", "Store C"]
#     # }
