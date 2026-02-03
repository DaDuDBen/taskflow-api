from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    title: str
    description: str | None = None

@app.get("/")
def root():
    return {"message": "TaskFlow API is alive"}

@app.post("/tasks")
def create_task(task: Task):
    return {
        "message": "Task created",
        "task": task
    }