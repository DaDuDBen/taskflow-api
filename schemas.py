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
        from_attributes = True

class PaginatedTasks(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[TaskResponse]

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
