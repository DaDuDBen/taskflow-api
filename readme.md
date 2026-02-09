# TaskFlow API

A simple backend REST API built with FastAPI to manage tasks.

## Features
- Create, read, update, and delete tasks
- In-memory data storage
- Proper HTTP status codes and validation
- Front-end demo dashboard at `/ui`

## Tech Stack
- Python
- FastAPI

## How to Run
```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/ui` to explore the TaskFlow dashboard.
