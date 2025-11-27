# Docker Guide

This guide explains how to build, run, and debug the FastAPI Recommender API using Docker.

---

# DOCKERFILE OVERVIEW

The project includes the following `Dockerfile`:

```Dockerfile
# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Expose port (FastAPI default)
EXPOSE 8000

# Run the FastAPI app via Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Key points:

- Uses **python:3.11-slim** for a lightweight container  
- Copies `requirements.txt` first → improves caching  
- Exposes port 8000  
- Starts the app with Uvicorn  

---

# .dockerignore

Ensure the file is correctly named `.dockerignore`.

Recommended contents:

```
__pycache__/
*.pyc
*.pyo
*.pyd
.env
.venv/
.git/
.gitignore
data/*.db
```

This keeps your Docker image:

- Smaller  
- Free of secrets  
- Free of local dev files  
- Free of SQLite artifacts unless intentionally persisted  

---

# BUILDING THE IMAGE

From the project root:

```bash
docker build -t fastapi-recommender .
```

Where:

- `fastapi-recommender` is the image name (you may choose any)

---

# RUNNING THE CONTAINER

Run the container and expose it on port `8000`:

```bash
docker run -d \
  --name fastapi-recommender \
  -p 8000:8000 \
  fastapi-recommender
```

Access the service:

- API: http://localhost:8000  
- Swagger UI: http://localhost:8000/docs  

---

# PASSING ENVIRONMENT VARIABLES

You can set env vars at runtime:

```bash
docker run -d \
  --name fastapi-recommender \
  -p 8000:8000 \
  -e ENVIRONMENT=deployment \
  -e DEBUG_MODE=False \
  fastapi-recommender
```

Or load all from `.env`:

```bash
docker run -d \
  --name fastapi-recommender \
  -p 8000:8000 \
  --env-file .env \
  fastapi-recommender
```

> Avoid baking secrets directly into the image.

---

# PERSISTING THE SQLITE DATABASE

By default, the SQLite DB inside the container is ephemeral.

To persist it:

```bash
docker run -d \
  --name fastapi-recommender \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  fastapi-recommender
```

Data is now stored on your host machine under `./data`.

---

# VIEWING LOGS

View container logs:

```bash
docker logs fastapi-recommender
```

Follow logs in real time:

```bash
docker logs -f fastapi-recommender
```

These logs include:

- Uvicorn access logs  
- Error messages  
- Custom request-timing log from `main.py`  

---

# OPEN A SHELL IN THE CONTAINER

To debug or inspect files:

```bash
docker exec -it fastapi-recommender /bin/bash
```

Inside the container you can:

- Check installed packages
- Explore `/app`
- Use the Python REPL

Exit with:

```
exit
```

---

# STOPPING AND REMOVING CONTAINERS

Stop:

```bash
docker stop fastapi-recommender
```

Remove:

```bash
docker rm fastapi-recommender
```

Remove the image:

```bash
docker rmi fastapi-recommender
```

---

# DOCKER + POSTMAN QUICK TEST

1. Start the container  
2. Open Postman  
3. Create request: `GET http://localhost:8000/health/ping`  
4. Expected response:

```json
{
  "message": "pong"
}
```

If this works, your Dockerized API is running correctly.

---

# SUMMARY

This guide covered:

- Dockerfile explanation  
- `.dockerignore` best practices  
- Building and running Docker containers  
- Debugging containers and logs  
- Persisting the SQLite database  
- Using Docker with Postman  

For deployment instructions, see **DEPLOYMENT.md**.  
For API specifications, see **API_REFERENCE.md**.
