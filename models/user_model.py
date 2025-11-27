from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str

    model_config = {
        "title": "User",
        "description": "A user object representing an individual user in the system.",
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "name": "Alice"
                },
                {
                    "id": 42,
                    "name": "Bob"
                }
            ]
        }
    }