from dataclasses import dataclass
from typing import Optional


@dataclass
class LineUserEntity:
    line_user_id: str
    user_name: str
    created_at: Optional[int] = None,
    updated_at: Optional[int] = None,

    def to_json(self):
        return {
            "line_user_id": self.line_user_id,
            "user_name": self.user_name,
        }
        pass
