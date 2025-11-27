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

