-- SQLite
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
WHERE user_id = 54;

SELECT user_id, merchant_id, MAX(transaction_count)
FROM (
    SELECT user_id, merchant_id, COUNT(*) AS transaction_count
    FROM spendings
    GROUP BY user_id, merchant_id
)
GROUP BY user_id