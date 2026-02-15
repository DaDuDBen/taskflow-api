from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from database import engine
from models import Base
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends
from models import Task
from schemas import TaskCreate, TaskResponse, PaginatedTasks
from fastapi import Query

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


@app.get("/tasks", response_model=PaginatedTasks)
def get_tasks(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    title: str | None = None
):
    query = db.query(Task)

    if title:
        query = query.filter(Task.title.ilike(f"%{title}%"))

    total = query.count()

    tasks = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": tasks
    }


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updated: TaskCreate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = updated.title
    task.description = updated.description
    db.commit()
    db.refresh(task)
    return task

    

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"success": True, "message": "Task deleted"}

