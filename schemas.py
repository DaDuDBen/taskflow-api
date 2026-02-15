from typing import List
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        orm_mode = True

class PaginatedTasks(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[TaskResponse]

    class Config:
        orm_mode = True