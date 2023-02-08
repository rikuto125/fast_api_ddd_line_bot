from dataclasses import dataclass
from typing import Optional


@dataclass
class StudentTaskEntity:
    id: str
    line_user_id: str
    task: str
    created_at: Optional[int] = None,
    updated_at: Optional[int] = None,

    def to_json(self):
        return {
            "line_user_id": self.line_user_id,
            "user_task": self.task,
        }
        pass
