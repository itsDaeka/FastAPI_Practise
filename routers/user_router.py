# routers/user_router.py

from fastapi import APIRouter, HTTPException, Query, Body
from models.user_model import User

router = APIRouter(
    tags=["users"]
)

# Example payloads for the /user endpoint
create_user_examples = {
    "normal": {
        "summary": "Typical user payload",
        "description": "A standard user object with an integer ID and a name.",
        "value": {
            "id": 1,
            "name": "Alice"
        },
    },
    "another": {
        "summary": "Another valid user",
        "description": "Demonstrates that any valid integer ID and string name are accepted.",
        "value": {
            "id": 42,
            "name": "Bob"
        },
    },
}


@router.post(
    "/user",
    summary="Echo a user payload",
    description="""
Accepts a **User** object in the request body and returns it back inside 
a wrapper object. This endpoint is primarily used to demonstrate:

- Pydantic model validation  
- JSON request body handling  
- How models appear in the OpenAPI schema  

### Responses
- **200 OK** – returns the received user object
""",
)
def create_user(
    user: User = Body(
        ...,
        openapi_examples=create_user_examples,
    )
):
    return {"received_user": user}


# Example payloads for the /check_name endpoint body
check_name_body_examples = {
    "ediz": {
        "summary": "Name matches 'ediz'",
        "description": "A request where the body contains the name `Ediz`, which should return `result: true`.",
        "value": {
            "name": "Ediz"
        },
    },
    "other": {
        "summary": "Name does not match 'ediz'",
        "description": "A request where the body contains a different name, which should return `result: false`.",
        "value": {
            "name": "Alice"
        },
    },
    "missing_name": {
        "summary": "Missing name field",
        "description": "A request with an empty body (or without `name`) results in `result: false`.",
        "value": {},
    },
}


@router.post(
    "/check_name",
    summary="Check if a name matches 'ediz'",
    description="""
Checks whether the provided `name` equals **`ediz`** (case-insensitive).

The name can be provided either:

- As a **query parameter**: `?name=Ediz`  
- Or in the **JSON body**: `{ "name": "Ediz" }`  

If both are provided, the body value is used (if present).

### Logic

1. Read `name` from the query string and/or request body.  
2. Normalize by lowercasing and trimming whitespace.  
3. Compare with the string `"ediz"`.  
4. Return a boolean result.

### Responses

- **200 OK**
  - `result: true` if name matches `"ediz"`.
  - `result: false` if name is missing or does not match.
""",
)
def check_name(
    name: str | None = Query(
        None,
        description="Optional name to check, provided as a query parameter.",
    ),
    name_body: dict | None = Body(
        None,
        openapi_examples=check_name_body_examples,
    ),
):
    # Determine the effective name
    if name_body is not None and isinstance(name_body, dict):
        if "name" in name_body and name_body["name"] is not None:
            name = name_body["name"]

    if not name:
        return {"name": None, "result": False}

    # Check condition
    result = name.lower().strip() == "ediz"
    return {"name": name, "result": result}


@router.get(
    "/divide",
    summary="Divide two integers",
    description="""
Divides integer `a` by integer `b` and returns the numeric result.

### Parameters

- `a` – dividend (integer)  
- `b` – divisor (integer, must not be zero)  

### Logic

- Validates that `b` is not zero.  
- Performs floating-point division (`a / b`).  
- Returns the result in a JSON object.

### Responses

- **200 OK** – division result returned successfully  
- **400 Bad Request** – if `b` is zero (`\"Cannot divide by zero\"`)
""",
)
def divide(a: int, b: int):
    if b == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    return {"result": a / b}
