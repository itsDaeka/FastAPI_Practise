# routers/user_router.py
from fastapi import APIRouter, HTTPException, Query, Body
from models.user_model import User

router = APIRouter(
    tags=["users"]
)

@router.post("/user")
def create_user(user: User):
    return {"received_user": user}

@router.post("/check_name")  # decorator to connect function to a HTTP endpoint
def check_name(
    name: str | None = Query(None),  # default to None
    name_body: dict | None = Body(None)
):
    # If not found in query, try to read from JSON body    
    if not name and name_body and "name" in name_body:
        name = name_body["name"]

    if not name:
        return {"name": None, "result": False}

    # Check condition
    result = name.lower().strip() == "ediz"
    return {"name": name, "result": result}

@router.get("/divide")
def divide(a: int, b: int):
    if b == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    return {"result": a / b}
