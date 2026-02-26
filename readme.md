# TaskFlow API

A lightweight, production-style task management backend built with **FastAPI**, **SQLAlchemy**, and **SQLite**.

TaskFlow API provides:

- JWT-based authentication
- User-scoped task CRUD (each user can only access their own tasks)
- Pagination and filtering for task lists
- Strong request/response validation using Pydantic
- Interactive API docs out of the box

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Running the API](#running-the-api)
- [Authentication Flow](#authentication-flow)
- [API Reference](#api-reference)
- [Example cURL Workflow](#example-curl-workflow)
- [Validation Rules](#validation-rules)
- [Testing](#testing)
- [Development Notes](#development-notes)

---

## Features

- **User registration & login**
- **JWT access tokens** using `python-jose`
- **Password hashing** using `passlib` + `bcrypt`
- **Full task CRUD** (`create`, `read`, `update`, `delete`)
- **Strict multi-user isolation** (querying by authenticated user)
- **Pagination + filtering** on `GET /tasks`
- **OpenAPI docs** via Swagger UI and ReDoc

---

## Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn
- python-jose
- passlib + bcrypt
- pytest
- ruff

---

## Project Structure

```text
.
├── main.py            # FastAPI app and route handlers
├── auth.py            # Password hashing, JWT creation, current-user auth dependency
├── config.py          # Environment-backed auth configuration
├── database.py        # SQLAlchemy engine/session setup
├── models.py          # SQLAlchemy models (User, Task)
├── schemas.py         # Pydantic request/response models
├── tests/             # API test suite
├── requirements.txt   # Python dependencies
└── readme.md
```

---

## Quick Start

### 1) Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Create an environment file

Create a `.env` file in the project root:

```env
SECRET_KEY=replace-with-a-long-random-secret
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

> `SECRET_KEY` is required for JWT signing.

### 4) Run the server

```bash
uvicorn main:app --reload
```

---

## Configuration

The app loads environment variables from `.env` using `python-dotenv`.

| Variable | Required | Default | Description |
|---|---|---|---|
| `SECRET_KEY` | Yes | _None_ | Secret used to sign JWT tokens |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `60` | Token expiration window in minutes |

JWT algorithm is currently fixed to `HS256` in `config.py`.

---

## Running the API

Once started, the API is available at:

- API base URL: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Health check/root endpoint:

```http
GET /
```

Response:

```json
{
  "message": "TaskFlow API is alive"
}
```

---

## Authentication Flow

1. **Register** via `POST /register`
2. **Login** via `POST /login` using form-encoded credentials
3. Receive a bearer token:
   ```json
   {
     "access_token": "<jwt-token>",
     "token_type": "bearer"
   }
   ```
4. Send token in headers for protected routes:
   ```http
   Authorization: Bearer <jwt-token>
   ```

---

## API Reference

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/` | No | Health/root message |
| `POST` | `/register` | No | Create a user account |
| `POST` | `/login` | No | Authenticate and get JWT token |
| `POST` | `/tasks` | Yes | Create a task |
| `GET` | `/tasks` | Yes | List tasks (with pagination/filtering) |
| `GET` | `/tasks/{task_id}` | Yes | Get one task by ID |
| `PUT` | `/tasks/{task_id}` | Yes | Update an existing task |
| `DELETE` | `/tasks/{task_id}` | Yes | Delete a task |

### `GET /tasks` query params

| Parameter | Type | Default | Constraints | Description |
|---|---|---|---|---|
| `limit` | `int` | `10` | `1 <= limit <= 100` | Number of items to return |
| `offset` | `int` | `0` | `offset >= 0` | Number of items to skip |
| `title` | `str` | _None_ | Optional | Case-insensitive partial title match |

Example:

```http
GET /tasks?limit=5&offset=0&title=report
```

---

## Example cURL Workflow

### Register

```bash
curl -X POST http://127.0.0.1:8000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"securepass123"}'
```

### Login

```bash
curl -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=alice&password=securepass123"
```

Copy `access_token` from the response, then:

```bash
TOKEN="<paste-token-here>"
```

### Create a task

```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Prepare sprint report","description":"Summarize completed tickets and blockers"}'
```

### List tasks

```bash
curl -X GET "http://127.0.0.1:8000/tasks?limit=10&offset=0" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Validation Rules

### User

- `username`: required, 3 to 50 characters
- `password`: required, minimum 6 characters

### Task

- `title`: required, 1 to 100 characters
- `description`: required, 1 to 500 characters

---

## Testing

Run all tests:

```bash
pytest
```

Run lint checks:

```bash
ruff check .
```

---

## Development Notes

- SQLite database file (`tasks.db`) is created automatically on first run.
- `PUT /tasks/{task_id}` currently expects a **full payload** (`title` + `description`), not a partial patch.
- The root endpoint can be used as a simple uptime/health probe.
