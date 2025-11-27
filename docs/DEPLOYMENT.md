# Deployment Guide

This document explains how to run the FastAPI Recommender API:

- Locally (development)
- In production mode
- On Render (example PaaS deployment)
- With environment variables

---

# PREREQUISITES

- Python **3.11+**
- `pip`
- Optional: `venv` or other virtual environment tools
- Optional: Docker (see `DOCKER_GUIDE.md`)

---

# ENVIRONMENT VARIABLES

All configuration values are loaded via `pydantic-settings` from:

- `.env` file  
- Actual OS environment variables  

### Supported environment keys:

| Variable | Description |
|---------|-------------|
| `APP_NAME` | Name of the application |
| `APP_VERSION` | Version string |
| `ENVIRONMENT` | `development` or `deployment` |
| `DEBUG_MODE` | `True` or `False` |
| `DATABASE_URL` | e.g. `sqlite:///data/spendings.db` |
| `API_KEY` | Example key (not used in routing yet) |

### Example `.env`

```env
APP_NAME="FastAPI Practice"
APP_VERSION="1.3.0"
ENVIRONMENT="development"
DEBUG_MODE=True
DATABASE_URL="sqlite:///data/spendings.db"
API_KEY="super-secret-key-123"
```

> In production: **do not** commit `.env` files. Use the hosting platform’s secret manager.

---

# LOCAL DEVELOPMENT

## 1. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate         # Linux/macOS
# .venv\Scripts\activate          # Windows

pip install --upgrade pip
pip install -r requirements.txt
```

Ensure `.env` is present.

---

## 2. Run the application (development mode)

```bash
uvicorn main:app --reload
```

- Hot reload enabled  
- Runs on port `8000`  

### Access the service:

- API root: http://localhost:8000  
- Swagger UI: http://localhost:8000/docs  
- ReDoc: http://localhost:8000/redoc  

---

# PRODUCTION-LIKE RUN (WITHOUT DOCKER)

To run the application in a more production-oriented mode:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Using multiple workers

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Common production enhancements (not included in repo):

- Reverse proxy (Nginx)
- HTTPS termination
- Rate-limiting / WAF
- Process manager (systemd, supervisor)

---

# DEPLOYING ON RENDER

Render is a PaaS suitable for simple deployments.

## 1. Push repository to GitHub/GitLab

Ensure the repository contains:

- `main.py`
- `requirements.txt`
- Optional: `Dockerfile` (Render can auto-detect)

---

## 2. Create Render Web Service

In Render Dashboard:

1. **New → Web Service**
2. Connect your repository
3. Choose:
   - Environment: **Python** (or Docker if using the Dockerfile)
   - Branch: main (or any you choose)

---

## If using Render’s Python runtime:

### Build Command
```bash
pip install -r requirements.txt
```

### Start Command
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Render sets `$PORT` automatically.

---

## If deploying using Docker:

Render will build using the project’s `Dockerfile` automatically:

- Ensure `Dockerfile` runs:

```Dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Render will map `$PORT` automatically if configured in settings.

---

# ENVIRONMENT VARIABLES ON RENDER

Go to:

**Render Dashboard → Service → Environment**

Set:

```
ENVIRONMENT=deployment
DEBUG_MODE=False
DATABASE_URL=sqlite:///data/spendings.db
API_KEY=<your-secret-key>
```

> ⚠ SQLite inside a container is fine for demos, but not recommended for real workloads.  
> For production: switch to PostgreSQL.

---

# DATABASE CONSIDERATIONS

### SQLite (current)
- Easy to set up
- Good for demos/small projects
- Lives in `data/spendings.db`

### For production use:
- PostgreSQL or MySQL recommended
- Use a connection string like:

```
postgresql+psycopg://user:password@hostname/dbname
```

- Migrations via Alembic recommended

---

# HEALTH CHECKS

### Readiness probe:
```
GET /health/ping
```

Success if:

```json
{ "message": "pong" }
```

Load balancers or uptime monitors can use this.

---

# POSTMAN WORKFLOW

Recommended Postman environment:

| Variable | Example |
|----------|---------|
| `baseUrl` | `http://localhost:8000` |

Example requests:

- `GET {{baseUrl}}/health/ping`
- `GET {{baseUrl}}/health/info`
- `POST {{baseUrl}}/spendings`
- `GET {{baseUrl}}/recommendations/1`

---

# SUMMARY

This guide covered:

- Local development workflow  
- Running and testing the API  
- Deploying with production-ready commands  
- Render cloud deployment  
- Managing environment variables  
- Database considerations  

For containerized deployment, see **DOCKER_GUIDE.md**.  
For detailed endpoint behavior, see **ENDPOINTS.md**.  
For API contract definitions, see **API_REFERENCE.md**.

