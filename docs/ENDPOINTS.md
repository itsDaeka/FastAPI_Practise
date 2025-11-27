# Endpoint Internals

This document explains **how the endpoints work under the hood**, including:

- Database interactions  
- Matrix logic  
- Recommendation logic  
- Dependency injection  
- Request handling patterns  

For the external API contract, see **API_REFERENCE.md**.  
For deployment details, see **DEPLOYMENT.md**.

---

# DATABASE LAYER

## SQLite Schema

The SQLite database is stored at:

```
data/spendings.db
```

The schema is created on startup via `create_table(DB_PATH)`:

```sql
CREATE TABLE IF NOT EXISTS spendings (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    merchant_id INTEGER NOT NULL,
    amount REAL NOT NULL
);
```

---

## Connection Management

`data/db.py` provides the reusable database utilities:

### `get_db()`

- Opens a SQLite connection
- Yields it to the endpoint
- Closes the connection afterward

Ensures **one connection per request**, reducing contention.

### `lifespan(app)`

Executed automatically by FastAPI:

1. Ensures the DB file exists  
2. Ensures the `spendings` table exists  
3. Seeds mock data (if enabled)  
4. Yields to allow the application to run  
5. Performs cleanup on shutdown  

---

## Data Seeding

`data/seed_data.py`:

- Generates mock spendings for:
  - 100 users  
  - 3 merchants  
- Inserts:
  - Randomized amounts  
  - Transaction rows

This provides realistic demo data for recommendation testing.

---

# SPENDINGS ENDPOINTS (Internal Logic)

Located in: `routers/spending_router.py`  
Models from: `models/spending_model.py`

---

## **POST /spendings**

### Internal flow:

1. FastAPI parses JSON body → `SpendingIn`
2. `db = Depends(get_db)` opens a per-request connection
3. SQL INSERT is executed
4. `cursor.lastrowid` is captured
5. A `SpendingOut` object is created and returned

This endpoint demonstrates:

- Validation via Pydantic  
- DB insertion  
- Returning structured models  

---

## **GET /spendings/{user_id}**

### Internal flow:

1. Path parameter parsed as `int`
2. Query:

```sql
SELECT transaction_id, user_id, merchant_id, amount
FROM spendings
WHERE user_id = ?;
```

3. Rows are converted into dictionaries
4. Each row is passed into `SpendingOut`
5. Response is a JSON list

This corresponds to retrieving a **row slice** of the implicit user–merchant matrix.

---

## **DELETE /spendings/{user_id}**

### Internal flow:

1. Retrieve all spendings for the user
2. Execute:

```sql
DELETE FROM spendings WHERE user_id = ?;
```

3. Wrap deleted records in `SpendingDeleted`
4. Return them as confirmation

Demonstrates **destructive operations** with reporting.

---

# MATRIX ENDPOINT (Internal Logic)

Located in: `routers/matrix_router.py`

## **GET /matrix_properties**

### Internal flow:

- Counts distinct users:

```sql
SELECT COUNT(DISTINCT user_id) FROM spendings;
```

- Counts distinct merchants:

```sql
SELECT COUNT(DISTINCT merchant_id) FROM spendings;
```

- Returns matrix shape:  
  `rows = users`, `cols = merchants`

This describes the **user × merchant** implicit matrix formed by transaction data.

---

# RECOMMENDATION ENDPOINT (Internal Logic)

Located in:  
- `routers/recommendation_router.py`  
- `services/recommender.py`

---

## Recommendation Query

`RecommenderService` uses SQL to determine the **most frequently used merchant** for the user.

### Core query:

```sql
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
```

### Interpretation:

- Count transactions per merchant per user  
- Find the merchant with the maximum count  
- Return that merchant  

If tied, any top-choice merchant may be selected.

---

## Service Structure

```python
class RecommenderService:
    def __init__(self, db):
        self.db = db

    def recommend(self, user_id: int):
        cursor = self.db.cursor()
        cursor.execute(RECOMMENDATION_QUERY, (user_id,))
        row = cursor.fetchone()
        return row["merchant_id"] if row else None
```

Encapsulates business logic cleanly, keeping routers simple.

---

## Dependency Injection

`get_recommender()` depends on `get_db()`:

```python
def get_recommender(db=Depends(get_db)):
    return RecommenderService(db)
```

Routers then inject services:

```python
@router.get("/{user_id}")
def get_recommendations(user_id: int, recommender=Depends(get_recommender)):
    return {
        "user_id": user_id,
        "recommended_merchant_id": recommender.recommend(user_id)
    }
```

This supports clean separation of:

- Routing  
- DB access  
- Business logic  

---

# HEALTH & USER ENDPOINTS (Internal Logic)

## **/health/ping**

- Static JSON return  
- No dependencies  
- Liveness probe  

## **/health/info**

- Depends on `get_settings()`  
- Shows environment metadata  

## **/user**

- Echo endpoint for demonstrating Pydantic body parsing  

## **/check_name**

- Accepts name via query or JSON  
- Case-insensitive comparison to `"ediz"`  

## **/divide**

- Validates divisor  
- Raises `HTTPException(400)` on division by zero  
- Returns computed result  

---

# DEPENDENCY INJECTION OVERVIEW

FastAPI’s DI is used for:

### Settings
- Loaded once via `@lru_cache`
- Injected into `/health/info`

### Database
- `get_db()` opens one connection per request

### Services
- Recomender service receives DB through DI
- Routers depend on service, not raw DB

This structure scales extremely well for larger APIs.

---

# MIDDLEWARE & LOGGING

`main.py` adds a timing middleware:

- Logs request method + path  
- Calculates elapsed time per request  
- Helps with debugging and performance insights  

---

# SUMMARY

This file described:

- How SQLite is accessed  
- How requests become queries  
- How the recommendation logic works  
- How FastAPI dependency injection ties the system together  

Use `API_REFERENCE.md` for request/response examples  
Use `DEPLOYMENT.md` for running the service  
Use `DOCKER_GUIDE.md` for containerization details  
