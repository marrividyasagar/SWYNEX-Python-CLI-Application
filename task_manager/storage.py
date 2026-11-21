"""JSON persistence layer for tasks."""
import json
from pathlib import Path
from task_manager.models import Task

class StorageError(Exception):
    """Raised when task data cannot be read or written safely."""

class TaskStorage:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self._write_tasks([])

    def _read_tasks(self):
        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
            if not isinstance(data, list):
                raise StorageError("Task data must be a JSON list.")
            return [Task.from_dict(item) for item in data]
        except json.JSONDecodeError as exc:
            raise StorageError(
                "The tasks file contains invalid JSON. Restore a valid backup "
                "or correct data/tasks.json."
            ) from exc
        except (OSError, TypeError, KeyError) as exc:
            raise StorageError(f"Could not read task data: {exc}") from exc

    def _write_tasks(self, tasks):
        try:
            with self.file_path.open("w", encoding="utf-8") as file:
                json.dump([task.to_dict() for task in tasks], file, indent=4)
        except OSError as exc:
            raise StorageError(f"Could not save task data: {exc}") from exc

    def get_all(self):
        return self._read_tasks()

    def add(self, title, description="", priority="medium", due_date=None):
        tasks = self._read_tasks()
        next_id = max((task.task_id for task in tasks), default=0) + 1
        from datetime import datetime
        task = Task(
            task_id=next_id,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            completed=False,
            created_at=datetime.now().isoformat(timespec="seconds")
        )
        tasks.append(task)
        self._write_tasks(tasks)
        return task

    def mark_completed(self, task_id):
        tasks = self._read_tasks()
        for task in tasks:
            if task.task_id == task_id:
                task.completed = True
                self._write_tasks(tasks)
                return task
        return None

    def delete(self, task_id):
        tasks = self._read_tasks()
        remaining = [task for task in tasks if task.task_id != task_id]
        if len(remaining) == len(tasks):
            return False
        self._write_tasks(remaining)
        return True
