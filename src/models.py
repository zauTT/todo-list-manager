from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    description: Optional[str]
    priority: str #high, medium, low
    due_date: Optional[str]
    completed: bool
    completed_at: Optional[str]
    created_at: str

    @classmethod
    def from_tuple(cls, task_tuple):
        return cls(
            id=task_tuple[0],
            title=task_tuple[1],
            description=task_tuple[2],
            priority=task_tuple[3],
            due_date=task_tuple[4],
            completed=task_tuple[5],
            completed_at=task_tuple[6],
            created_at=task_tuple[7]
        )

    def is_overdue(self) -> bool:
        if not self.due_date or self.completed:
            return False

        due=datetime.fromisoformat(self.due_date).date()
        return due < datetime.now().date()

    def status_text(self) -> str:
        return '✓ Done' if self.completed else '○ Pending'

