
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Time
from sqlalchemy.sql import func
from app.database import Base
from pydantic import BaseModel
from typing import Annotated
import re

DateStr = Annotated[str, re.compile(r"^\d{4}-\d{2}-\d{2}$")]


class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    frequency = Column(String, nullable=False)  # e.g., daily, weekly
    target_count = Column(Integer, nullable=False)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    reminder_time = Column(Time, nullable=True)  # e.g., "09:00"
    category = Column(String, nullable=True)  # e.g., Health, Productivity
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

