# API Reference

This document specifies the **public HTTP API** exposed by the FastAPI Recommender service.

For internal implementation details, see **ENDPOINTS.md**.  
For deployment details, see **DEPLOYMENT.md**.

---

## Conventions

- **Base URL (local):** `http://localhost:8000`
- **Content Type:** `application/json`
- **Error format:** Standard FastAPI error structure:

```json
{
  "detail": "Error message"
}
```

---

# HEALTH ENDPOINTS

## **GET /health/ping**

**Summary:** Liveness probe — always returns `"pong"` if the service is reachable.

### Response 200
```json
{
  "message": "pong"
}
```

---

## **GET /health/info**

**Summary:** Returns application metadata and environment configuration.

### Response 200 (example)
```json
{
  "app": "FastAPI Practise",
  "version": "0.1.0",
  "environment": "development",
  "debug": true,
  "database": "sqlite:///data/spendings.db"
}
```

---

# USER ENDPOINTS

## **POST /user**

Echoes a user payload back to the client. Demonstrates Pydantic model handling.

### Request Body
```json
{
  "id": 1,
  "name": "Alice"
}
```

### Response 200
```json
{
  "received_user": {
    "id": 1,
    "name": "Alice"
  }
}
```

---

## **POST /check_name**

Checks whether the provided name matches `"ediz"` (case-insensitive).

### Query Param (optional)
| Name | Type | Required | Description |
|------|------|----------|-------------|
| name | string | No | Name to check |

### OR Request Body
```json
{
  "name": "Ediz"
}
```

### Response 200
```json
{
  "name": "Ediz",
  "result": true
}
```

If no name was provided:
```json
{
  "name": null,
  "result": false
}
```

---

## **GET /divide**

Performs division (`a / b`). Demonstrates query parameters and error handling.

### Query Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| a | int | Yes | Dividend |
| b | int | Yes | Divisor (must not be 0) |

### Response 200
```json
{
  "result": 2.5
}
```

### Response 400 (b = 0)
```json
{
  "detail": "Cannot divide by zero"
}
```

---

# SPENDINGS ENDPOINTS

These endpoints operate on the SQLite `spendings` table.

### Models

**SpendingIn**
```json
{
  "user_id": 1,
  "merchant_id": 2,
  "amount": 42.5
}
```

**SpendingOut**
```json
{
  "transaction_id": 10,
  "user_id": 1,
  "merchant_id": 2,
  "amount": 42.5
}
```

**SpendingDeleted**
```json
{
  "transaction_id": 10,
  "user_id": 1,
  "merchant_id": 2,
  "amount": 42.5,
  "deleted": true
}
```

---

## **POST /spendings**

Creates a new spending row.

### Request Body
```json
{
  "user_id": 1,
  "merchant_id": 2,
  "amount": 19.99
}
```

### Response 201/200
```json
{
  "transaction_id": 123,
  "user_id": 1,
  "merchant_id": 2,
  "amount": 19.99
}
```

---

## **GET /spendings/{user_id}**

Fetch all spendings for a given user.

### Response 200
```json
[
  {
    "transaction_id": 101,
    "user_id": 1,
    "merchant_id": 1,
    "amount": 12.5
  },
  {
    "transaction_id": 102,
    "user_id": 1,
    "merchant_id": 2,
    "amount": 8.0
  }
]
```

If none:
```json
[]
```

---

## **DELETE /spendings/{user_id}**

Deletes all spendings for a user and returns the deleted records.

### Response 200
```json
[
  {
    "transaction_id": 101,
    "user_id": 1,
    "merchant_id": 1,
    "amount": 12.5,
    "deleted": true
  }
]
```

---

# MATRIX ENDPOINTS

## **GET /matrix_properties**

Returns the implicit spending matrix's dimensions (users × merchants).

### Response 200
```json
{
  "rows": 100,
  "cols": 3,
  "note": "Number of rows correspond to number of users, and columns correspond to number of merchants."
}
```

---

# RECOMMENDATION ENDPOINTS

## **GET /recommendations/{user_id}**

Returns the merchant most frequently used by the specified user.

### Response 200
```json
{
  "user_id": 1,
  "recommended_merchant_id": 2
}
```

If no recommendation exists:
```json
{
  "user_id": 999,
  "recommended_merchant_id": null
}
```

---

# POSTMAN NOTES

To test the API using Postman:

- Use **Body → raw → JSON** for POST requests.
- Example sequence:
  - `GET /health/ping`
  - `POST /spendings`
  - `GET /spendings/1`
  - `GET /recommendations/1`

The API is designed to integrate easily with standard REST tooling.