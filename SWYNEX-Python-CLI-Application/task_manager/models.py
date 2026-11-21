"""Task model and validation helpers."""
from dataclasses import dataclass, asdict
from datetime import date
from typing import Optional

VALID_PRIORITIES = {"low", "medium", "high"}

@dataclass
class Task:
    task_id: int
    title: str
    description: str = ""
    priority: str = "medium"
    due_date: Optional[str] = None
    completed: bool = False
    created_at: str = ""

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

def validate_title(title: str) -> str:
    cleaned = title.strip()
    if not cleaned:
        raise ValueError("Task title cannot be empty.")
    if len(cleaned) > 100:
        raise ValueError("Task title must be 100 characters or fewer.")
    return cleaned

def validate_priority(priority: str) -> str:
    cleaned = priority.strip().lower()
    if cleaned not in VALID_PRIORITIES:
        raise ValueError("Priority must be low, medium, or high.")
    return cleaned

def validate_due_date(value: str):
    cleaned = value.strip()
    if not cleaned:
        return None
    try:
        date.fromisoformat(cleaned)
    except ValueError as exc:
        raise ValueError("Date must use YYYY-MM-DD format.") from exc
    return cleaned
