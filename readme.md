# TaskFlow API

TaskFlow API is a lightweight REST service for managing tasks, built with **FastAPI**, **SQLAlchemy**, and **SQLite**.

## Features

- Create, read, update, and delete tasks.
- Request validation with Pydantic schemas.
- Paginated task listing with optional title filtering.
- SQLite persistence (data stored in `tasks.db`).
- Automatic interactive docs via Swagger UI and ReDoc.

## Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn

## Project Structure

```text
.
├── main.py       # FastAPI application and routes
├── database.py   # Database engine/session setup
├── models.py     # SQLAlchemy models
├── schemas.py    # Pydantic request/response schemas
└── readme.md
```

## Getting Started

### 1) Install dependencies

```bash
pip install fastapi uvicorn sqlalchemy
```

### 2) Run the API

```bash
uvicorn main:app --reload
```

By default, the server runs at:

- API base URL: `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`
- ReDoc docs: `http://127.0.0.1:8000/redoc`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health/root message |
| `POST` | `/tasks` | Create a task |
| `GET` | `/tasks` | List tasks with pagination and optional title filter |
| `GET` | `/tasks/{task_id}` | Get a single task by ID |
| `PUT` | `/tasks/{task_id}` | Update a task |
| `DELETE` | `/tasks/{task_id}` | Delete a task |

## Query Parameters for `GET /tasks`

- `limit` (default: `10`, min: `1`, max: `100`)
- `offset` (default: `0`, min: `0`)
- `title` (optional, case-insensitive partial match)

Example:

```http
GET /tasks?limit=5&offset=0&title=report
```

## Request / Response Examples

### Create Task

**Request**

```json
{
  "title": "Prepare sprint report",
  "description": "Summarize completed tickets and blockers"
}
```

**Response (`201 Created`)**

```json
{
  "id": 1,
  "title": "Prepare sprint report",
  "description": "Summarize completed tickets and blockers"
}
```

### List Tasks

**Response (`200 OK`)**

```json
{
  "total": 1,
  "limit": 10,
  "offset": 0,
  "items": [
    {
      "id": 1,
      "title": "Prepare sprint report",
      "description": "Summarize completed tickets and blockers"
    }
  ]
}
```

## Validation Rules

- `title`: required, 1 to 100 characters.
- `description`: required, 1 to 500 characters.

## Notes

- The SQLite database file (`tasks.db`) is created automatically on first run.
- `PUT /tasks/{task_id}` currently expects a full task payload (title + description).
