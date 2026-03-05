from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Task, Lesson, UserMemory
from schemas import TaskCreate, TaskUpdate, TaskResponse, LessonCreate, LessonResponse, UserMemoryCreate, UserMemoryResponse

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- TASKS ---

@router.post("/tasks/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(
        title=task.title,
        description=task.description,
        status="active",
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db_task.status = task_update.status
    if task_update.status == "completed":
        db_task.end_time = datetime.utcnow()

    if task_update.emotion:
        db_task.emotion = task_update.emotion
    if task_update.skill_gap_tags:
        db_task.skill_gap_tags = task_update.skill_gap_tags

    db.commit()
    db.refresh(db_task)
    return db_task

# --- LESSONS (for completed tasks) ---

@router.post("/tasks/{task_id}/lesson", response_model=LessonResponse)
def create_lesson(task_id: int, lesson: LessonCreate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    if db_task.status != "completed":
        raise HTTPException(status_code=400, detail="Task must be completed to create lesson")

    db_lesson = Lesson(
        task_id=task_id,
        summary=lesson.summary,
        key_skills=lesson.key_skills,
        mistakes=lesson.mistakes,
        tips=lesson.tips,
    )
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

@router.get("/tasks/{task_id}/lesson", response_model=LessonResponse)
def get_lesson(task_id: int, db: Session = Depends(get_db)):
    db_lesson = db.query(Lesson).filter(Lesson.task_id == task_id).first()
    if not db_lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return db_lesson

# --- TASK SEARCH (simplified) ---

@router.get("/tasks/search")
def search_tasks(query: str, db: Session = Depends(get_db)):
    if not query:
        return []
    tasks = db.query(Task).filter(Task.title.contains(query) | Task.description.contains(query)).all()
    return tasks

# --- USER MEMORY (multi‑turn) ---

@router.post("/sessions/message", response_model=UserMemoryResponse)
def store_message(message: UserMemoryCreate, db: Session = Depends(get_db)):
    # Count how many turns exist for this session
    last_turn = db.query(UserMemory).filter(UserMemory.session_id == message.session_id).count()
    new_turn = last_turn + 1

    db_memory = UserMemory(
        session_id=message.session_id,
        turn=new_turn,
        user_input=message.user_input,
        ai_response=message.ai_response,
        task_hint=message.task_hint,
    )
    db.add(db_memory)
    db.commit()
    db.refresh(db_memory)
    return db_memory

@router.get("/sessions/{session_id}")
def get_session_memory(session_id: str, db: Session = Depends(get_db)):
    messages = db.query(UserMemory).filter(UserMemory.session_id == session_id).all()
    return messages
