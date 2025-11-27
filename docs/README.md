# FastAPI Recommender API

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.122.0-brightgreen.svg)
![Docker](https://img.shields.io/badge/Docker-ready-informational.svg)
![SQLite](https://img.shields.io/badge/DB-SQLite-lightgrey.svg)

A FastAPI-based backend service that simulates a **recommender system** on top of a **SQLite** spending dataset.  
It is designed as a **learning project** but structured to resemble a **production-style** backend, with clear separation of concerns, dependency injection, and Docker-ready deployment.

---

## Overview

The service exposes endpoints for:

- Health checks and runtime info
- Simple user-related operations
- Managing spendings (write and read from SQLite)
- Inspecting the user–merchant spending matrix
- Getting merchant recommendations for a user

The project is structured to be understandable for:

- **Backend engineers** (FastAPI, DB, routing)
- **ML engineers** (data layout, recommendation logic)
- **DevOps engineers** (Docker, deployment, configuration)

---

## Architecture

High-level architecture:

```text
FastAPI Application
 ├── Routers (HTTP endpoints)
 │   ├── /health
 │   ├── /user, /check_name, /divide
 │   ├── /spendings
 │   ├── /matrix_properties
 │   └── /recommendations/{user_id}
 ├── Services
 │   └── RecommenderService (SQL-based recommendation)
 ├── Data Layer
 │   ├── SQLite DB + connection management
 │   └── Seed script to generate mock spendings
 └── Configuration
     └── Pydantic BaseSettings + .env
```

## Key ideas:

- Routers define HTTP endpoints grouped by concern.
- Services encapsulate business logic (e.g., recommendations).
- Data layer manages SQLite DB, schema creation, and seeding.
- Config uses pydantic-settings to load settings from `.env`.
- Lifespan handler ensures the DB is initialized when the app starts.

---

## Folder Structure

From the project root:

~~~text
fastapi_practise/
├── main.py                 # FastAPI app entrypoint (logging, routers, lifespan)
├── config/
│   ├── __init__.py
│   └── settings.py         # Settings via BaseSettings (env-based)
├── data/
│   ├── __init__.py         # DB_PATH + create_table
│   ├── db.py               # get_db() + lifespan()
│   ├── seed_data.py        # Mock data generator for spendings
│   └── spendings.db        # SQLite database (generated)
├── models/
│   ├── user_model.py       # User Pydantic model
│   └── spending_model.py   # SpendingIn / SpendingOut / SpendingDeleted
├── routers/
│   ├── __init__.py         # Re-exports routers
│   ├── health_router.py
│   ├── user_router.py
│   ├── spending_router.py
│   ├── matrix_router.py
│   └── recommendation_router.py
├── services/
│   └── recommender.py      # RecommenderService (SQL-based)
├── Dockerfile              # Container definition
├── .dockerignore           # Docker build context exclusions (recommended name)
├── requirements.txt        # Python dependencies
└── .env                    # Local environment configuration
~~~

> Note: Ensure `.dockerigore` is renamed to `.dockerignore` so Docker can use it.

---

## Tech Stack

- **Language:** Python 3.11+
- **Web Framework:** FastAPI
- **ASGI Server:** Uvicorn
- **Database:** SQLite (file-based)
- **Config Management:** pydantic-settings
- **Containerization:** Docker

---

## Quickstart (Local Development)

### Clone the repository
```bash
git clone <your-repo-url>.git
cd fastapi_practise
```

## Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
# .venv\Scripts\activate    # Windows
```

## Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Check or configure `.env`

Example:

```env
APP_NAME="FastAPI Practice"
APP_VERSION="1.3.0"
ENVIRONMENT="development"
DEBUG_MODE=True
DATABASE_URL="sqlite:///data/spendings.db"
API_KEY="super-secret-key-123"
```

## Run the API

```bash
uvicorn main:app --reload
```

## Open the interactive docs

- Swagger UI: http://localhost:8000/docs  
- ReDoc: http://localhost:8000/redoc

---

## Where to Go Next

- Detailed endpoint specs: `API_REFERENCE.md`  
- Internal logic (spendings, matrix, recommendations): `ENDPOINTS.md`  
- Deployment instructions (local & Render): `DEPLOYMENT.md`  
- Docker usage & debug: `DOCKER_GUIDE.md`

---

## Limitations & Future Improvements

This is a learning-focused implementation, not a full production recommender system.

### Current limitations:

- **SQLite is used as a local file-based DB:**
  - Not suitable for high-concurrency or large-scale deployments.
  - Data may not persist across container restarts unless volumes are configured.

- **Recommendation logic:**
  - Uses a simple SQL-based heuristic (most frequently used merchant per user).
  - No collaborative filtering, ranking, or ML-based scoring.

- **User endpoints:**
  - `/user` is currently a simple echo endpoint (no persistence).
  - `/check_name` is a didactic example, not a real-world check.

- **Error handling and validation:**
  - Enough for demos, but minimal compared to a hardened production API.

### Potential improvements:

- Replace SQLite with PostgreSQL (or another production-ready DB).  
- Introduce a real recommendation model (e.g., collaborative filtering, embeddings).  
- Add authentication/authorization (API keys, OAuth, JWT).  
- Add richer user & merchant models and endpoints.  
- Extend test coverage and CI/CD integration.