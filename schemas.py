from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# =========================
# TASK SCHEMAS
# =========================

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    end_time: Optional[datetime] = None
    emotion: Optional[str] = None
    skill_gap_tags: Optional[str] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    emotion: Optional[str] = None
    skill_gap_tags: Optional[str] = None

    class Config:
        from_attributes = True


# =========================
# LESSON SCHEMAS
# =========================

class LessonCreate(BaseModel):
    task_id: int
    summary: str


class LessonResponse(BaseModel):
    id: int
    task_id: int
    summary: str

    class Config:
        from_attributes = True


# =========================
# USER MEMORY SCHEMAS
# =========================

class UserMemoryCreate(BaseModel):
    content: str


class UserMemoryResponse(BaseModel):
    id: int
    content: str

    class Config:
        from_attributes = True