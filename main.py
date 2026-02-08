from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from database import engine
from models import Base
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends
from models import Task
from schemas import TaskCreate, TaskResponse


Base.metadata.create_all(bind=engine)

app = FastAPI()
tasks_db = []
task_id_counter = 1

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

def find_task_by_id(task_id: int):
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    return None

def find_task_index(task_id: int):
    for index, task in enumerate(tasks_db):
        if task["id"] == task_id:
            return index
    return None

@app.get("/")
def root():
    return {"message": "TaskFlow API is alive"}

@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(
        title=task.title,
        description=task.description
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.get("/tasks")
def get_tasks():
    return tasks_db

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = find_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskUpdate):
    task = find_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task["id"] == task_id:
        if updated_task.title is not None:
            task["title"] = updated_task.title
        if updated_task.description is not None:
            task["description"] = updated_task.description
        return task
    

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    index = find_task_index(task_id)
    if index is None:
        raise HTTPException(status_code=404, detail="Task not found")

    deleted_task = tasks_db.pop(index)
    return {
        "message": "Task deleted",
        "task": deleted_task
    }
