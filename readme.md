# TaskFlow API

TaskFlow API is a lightweight task management backend built with **FastAPI**, **SQLAlchemy**, and **SQLite**. It includes JWT-based authentication and user-scoped task management.

## Features

- User registration and login.
- JWT access token authentication.
- Full CRUD operations for tasks.
- Per-user task isolation (users can only access their own tasks).
- Paginated task listing with optional title filtering.
- Request and response validation with Pydantic schemas.
- Interactive API docs via Swagger UI and ReDoc.

## Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn
- python-jose + passlib (JWT and password hashing)

## Project Structure

```text
.
├── main.py          # FastAPI app and route handlers
├── auth.py          # Password hashing, token creation, auth dependency
├── database.py      # Database engine/session setup
├── models.py        # SQLAlchemy models
├── schemas.py       # Pydantic request/response models
├── requirements.txt # Project dependencies
└── readme.md
```

## Getting Started

### 1) Install dependencies

```bash
pip install -r requirements.txt
```

### 2) Run the API

```bash
uvicorn main:app --reload
```

By default, the server runs at:

- API base URL: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Authentication Flow

1. Create a user with `POST /register`.
2. Log in with `POST /login` using form fields (`username`, `password`) to receive a bearer token.
3. Click **Authorize** in Swagger UI (or send an `Authorization: Bearer <token>` header) for protected task endpoints.

## API Endpoints

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| `GET` | `/` | No | Health/root message |
| `POST` | `/register` | No | Create a user account |
| `POST` | `/login` | No | Get JWT token |
| `POST` | `/tasks` | Yes | Create a task |
| `GET` | `/tasks` | Yes | List tasks with pagination and optional title filter |
| `GET` | `/tasks/{task_id}` | Yes | Get one task by ID |
| `PUT` | `/tasks/{task_id}` | Yes | Update a task |
| `DELETE` | `/tasks/{task_id}` | Yes | Delete a task |

## Query Parameters (`GET /tasks`)

- `limit` (default: `10`, min: `1`, max: `100`)
- `offset` (default: `0`, min: `0`)
- `title` (optional, case-insensitive partial match)

Example:

```http
GET /tasks?limit=5&offset=0&title=report
```

## Request / Response Examples

### Register

**Request**

```json
{
  "username": "alice",
  "password": "securepass123"
}
```

### Login

**Request (`application/x-www-form-urlencoded`)**

```text
username=alice&password=securepass123
```

**Response (`200 OK`)**

```json
{
  "access_token": "<jwt-token>",
  "token_type": "bearer"
}
```

### Create Task

**Request**

```json
{
  "title": "Prepare sprint report",
  "description": "Summarize completed tickets and blockers"
}
```

**Response (`200 OK`)**

```json
{
  "id": 1,
  "title": "Prepare sprint report",
  "description": "Summarize completed tickets and blockers"
}
```

## Validation Rules

### Task

- `title`: required, 1 to 100 characters.
- `description`: required, 1 to 500 characters.

### User

- `username`: required, 3 to 50 characters.
- `password`: required, minimum 6 characters.

## Notes

- The SQLite database file (`tasks.db`) is created automatically on first run.
- `PUT /tasks/{task_id}` currently expects a full task payload (`title` and `description`).
