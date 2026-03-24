# Containerised API Deployment Project

A production-ready REST API built with FastAPI, containerised with Docker, and deployed to the cloud via a fully automated CI/CD pipeline using GitHub Actions.

**Live API:** https://task-api-latest-ljxo.onrender.com  
**Interactive Docs:** https://task-api-latest-ljxo.onrender.com/docs

---

## Overview

This project was built to strengthen skills in backend development, containerisation, and modern deployment practices. It demonstrates a complete software delivery pipeline — from writing code locally to shipping a live, publicly accessible service automatically on every push.

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| API Framework | FastAPI | REST API with automatic validation and docs |
| Server | Uvicorn | ASGI server to run FastAPI |
| Validation | Pydantic | Data modelling and environment config |
| Testing | Pytest + HTTPX | Automated endpoint testing |
| Containerisation | Docker | Consistent runtime across all environments |
| Image Registry | Docker Hub | Stores and distributes the Docker image |
| CI/CD | GitHub Actions | Automated testing, building, and pushing |
| Cloud Platform | Render | Hosts and serves the live container |

---

## Project Structure

```
Containerised-API-Deployment-Project/
├── .github/
│   └── workflows/
│       └── deploy.yml        # CI/CD pipeline definition
├── app/
│   ├── __init__.py
│   ├── main.py               # App entry point, logging setup
│   ├── models.py             # Pydantic data models
│   ├── routes.py             # API endpoint definitions
│   └── config.py             # Environment variable configuration
├── tests/
│   ├── __init__.py
│   └── test_main.py          # Automated endpoint tests
├── .dockerignore             # Files excluded from Docker build
├── .gitignore                # Files excluded from Git
├── Dockerfile                # Container build instructions
└── requirements.txt          # Python dependencies
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check — confirms API is running |
| `GET` | `/tasks` | Returns all tasks |
| `POST` | `/tasks` | Creates a new task |
| `GET` | `/tasks/{task_id}` | Returns a single task by ID |
| `DELETE` | `/tasks/{task_id}` | Deletes a task by ID |

### Example Request

```bash
curl -X POST https://task-api-latest-ljxo.onrender.com/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Docker", "description": "Containerise the API", "completed": false}'
```

### Example Response

```json
{
  "message": "Task created",
  "task": {
    "title": "Learn Docker",
    "description": "Containerise the API",
    "completed": false
  }
}
```

---

## CI/CD Pipeline

Every push to the `main` branch triggers the following automated pipeline:

```
git push
    ↓
GitHub Actions spins up Ubuntu VM
    ↓
Installs dependencies
    ↓
Runs 8 automated tests
    ↓
Tests pass → builds Docker image
    ↓
Pushes image to Docker Hub
    ↓
Render pulls latest image and redeploys
    ↓
Live API updated automatically
```

If any test fails, the pipeline stops — no broken code ever reaches production.

---

## Running Locally

### With Python

```bash
# Clone the repo
git clone https://github.com/Ramshri-Mohapatra/Containerised-API-Deployment-Project.git
cd Containerised-API-Deployment-Project

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "APP_NAME=Task Manager API" > .env
echo "APP_VERSION=1.0.0" >> .env
echo "DEBUG=True" >> .env

# Run the API
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for the interactive documentation.

### With Docker

```bash
# Pull the image from Docker Hub
docker pull rskishanrk/task-api:latest

# Run the container
docker run -p 8000:8000 rskishanrk/task-api:latest
```

No Python installation required.

---

## Running Tests

```bash
pytest tests/ -v
```

Expected output:

```
tests/test_main.py::test_root                      PASSED
tests/test_main.py::test_get_tasks_empty           PASSED
tests/test_main.py::test_create_task               PASSED
tests/test_main.py::test_create_task_missing_title PASSED
tests/test_main.py::test_get_task                  PASSED
tests/test_main.py::test_get_task_not_found        PASSED
tests/test_main.py::test_delete_task               PASSED
tests/test_main.py::test_delete_task_not_found     PASSED

8 passed
```

Tests cover both valid inputs (happy path) and invalid inputs (unhappy path) including missing required fields and non-existent task IDs.

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name shown in docs | `Task Manager API` |
| `APP_VERSION` | API version | `1.0.0` |
| `DEBUG` | Enables debug-level logging | `True` |

Locally these are set in a `.env` file. In production they are configured directly in Render's environment settings. The `.env` file is never committed to version control.

---

## Docker Hub

The image is publicly available at:

```
docker pull rskishanrk/task-api:latest
```

https://hub.docker.com/r/rskishanrk/task-api

---

## Key Concepts Demonstrated

**Separation of concerns** — models, routes, config, and entry point are each in dedicated files with single responsibilities.

**Data validation** — Pydantic automatically validates all incoming request data against defined models, rejecting malformed requests before they reach business logic.

**Environment-based configuration** — no hardcoded secrets or settings. Behaviour changes per environment (local vs production) by changing environment variables alone.

**Structured logging** — timestamped, severity-levelled logs with file-level attribution across the codebase. Log level controlled via environment variable.

**Test independence** — pytest fixtures clear shared state before and after every test, ensuring tests never affect each other.

**Layer caching** — Dockerfile structured to copy and install dependencies before copying application code, maximising Docker's build cache efficiency.

**Pipeline safety gate** — CI/CD pipeline is structured so the build and push job only runs if all tests pass. Broken code cannot reach production.
