from datetime import datetime

from pydantic import BaseModel


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    due_date: datetime
    priority: str
    status: str
    creator_id: int
    assigned_to_id: int


class TodoCreate(BaseModel):
    title: str
    description: str
    due_date: datetime
    priority: str
    status: str = 'open'
    creator_id: int
    assigned_to_id: int = None


class TodoUpdate(BaseModel):
    title: str = None
    description: str = None
    status: str = None
