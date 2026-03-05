from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# -------- TASKS TABLE ----------
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="active")  # active, completed, paused
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    emotion = Column(String(50), nullable=True)          # will come from Task 1 later
    skill_gap_tags = Column(String(500), nullable=True)   # "python,sql,debugging"

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}')>"

# -------- LESSONS TABLE ----------
class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    summary = Column(Text, nullable=False)
    key_skills = Column(String(500), nullable=True)      # "python,sql"
    mistakes = Column(Text, nullable=True)
    tips = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Lesson(id={self.id}, task_id={self.task_id})>"

# -------- USER MEMORY (turns) ----------
class UserMemory(Base):
    __tablename__ = "user_memory"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), nullable=False)    # e.g., "user_task_1_session"
    turn = Column(Integer, nullable=False)              # 1st turn, 2nd turn, etc.
    user_input = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    task_hint = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<UserMemory(session_id='{self.session_id}', turn={self.turn})>"
