"""
RecommenderService

A very simple SQL-based recommender algorithm.

Current Logic:
- For each user, count how many times they used each merchant
- Select the merchant with the highest usage
- Return that merchant_id

Limitations:
- No ranking
- No ML
- No similarity scoring
- No embeddings
- No collaborative filtering
"""

import sqlite3

RECOMMENDATION_QUERY = """
SELECT merchant_id
FROM (
    SELECT user_id, merchant_id, COUNT(*) AS transaction_count
    FROM spendings s
    GROUP BY user_id, merchant_id
    HAVING COUNT(*) = (
        SELECT COUNT(*)
        FROM spendings s2
        WHERE s2.user_id = s.user_id
        GROUP BY merchant_id
        ORDER BY COUNT(*) DESC
        LIMIT 1
    )
)
WHERE user_id = ?;
"""

class RecommenderService:
    def __init__(self, db: sqlite3.Connection):
        self.db = db

    def recommend(self, user_id: int) -> int | None:
        cursor = self.db.cursor()
        cursor.execute(RECOMMENDATION_QUERY, (user_id,))
        row = cursor.fetchone()
        return row["merchant_id"] if row else None
