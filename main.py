from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
tasks_db = []
task_id_counter = 1

class Task(BaseModel):
    title: str
    description: str | None = None

@app.get("/")
def root():
    return {"message": "TaskFlow API is alive"}

@app.post("/tasks")
def create_task(task: Task):
    global task_id_counter

    new_task = {
        "id": task_id_counter,
        "title": task.title,
        "description": task.description
    }

    tasks_db.append(new_task)
    task_id_counter += 1

    return new_task

@app.get("/tasks")
def get_tasks():
    return tasks_db
