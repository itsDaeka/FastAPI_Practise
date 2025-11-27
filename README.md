# FastAPI Practice Project

A structured FastAPI project designed to simulate a small backend system, including:

- A health check service  
- User utilities  
- Spending storage endpoints  
- Matrix dimension generation  
- A simple rule-based recommendation engine  
- Dependency injection  
- Database initialization and seeding  
- Logging middleware  
- Dockerized deployment  
- Render deployment (production)

This project is used for hands-on learning of backend development concepts used in professional machine learning & API engineering teams.

# Project Documentation

See the full docs in the [`docs/`](docs/) directory:

- [Index](docs/INDEX.md)
- [API Reference](docs/API_REFERENCE.md)
- [Endpoints](docs/ENDPOINTS.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Docker Guide](docs/DOCKER_GUIDE.md)

---

## 📐 Architecture Overview

The application is structured as a modular FastAPI service:

```
FastAPI App  
│
├── Routers (modular endpoints)
├── Models (Pydantic schemas)
├── Services (business logic)
├── Data (SQLite + seeding)
├── Config (environment settings)
├── Docker (containerization)
└── Logging + Middleware
```

The system stores synthetic “spending” records in a local SQLite database and provides:

- CRUD-like spending endpoints  
- A matrix properties endpoint  
- A simple SQL-based recommendation engine  
- Health and info endpoints with environment introspection  

---

## 🗂 Folder Structure

```
fastapi_practise
├── config/               # Pydantic BaseSettings (env + config)
├── data/                 # SQLite DB, table creation, seed generator
├── models/               # Pydantic request/response models
├── routers/              # All FastAPI route modules
├── services/             # RecommenderService business logic
├── main.py               # App entry point + middleware
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker image definition
├── .dockerignore         # Files excluded from the Docker image
└── .env                  # Environment variables
```

---

## 🛠 Tech Stack

- **FastAPI** (web framework)
- **SQLite** (lightweight local database)
- **Uvicorn** (ASGI server)
- **Pydantic v2 + pydantic-settings** (validation & configuration)
- **NumPy** (synthetic data generation)
- **Render** (deployment)
- **Docker** (containerization)
- **Python 3.11**

---

## ▶️ Running the Project

### Local (dev mode)

```
uvicorn main:app --reload
```

### Production-like mode

```
uvicorn main:app --host 0.0.0.0 --port 8080
```

### Docker

```
docker build -t fastapi-practise .
docker run -p 8000:8000 fastapi-practise
```

---

## 📄 API Documentation

Once running:

- Interactive docs: **`/docs`**  
- ReDoc documentation: **`/redoc`**

---

## ✔ Goal of This Project

This project serves as a full learning path through:

- API design  
- JSON parsing  
- Query vs body parameters  
- Dependency injection  
- Database usage  
- Deployment  
- Dockerization  
- Logging  
- Modular code architecture  

It is intentionally structured to be similar to real-world ML + backend hybrid projects.
