from datetime import datetime
from typing import Union
from sqlalchemy import Column, Integer, String

from domain.student_task.student_task import StudentTaskEntity
from driver.rdb import Base


def unixTimestamp() -> int:
    # 後で日本時間にする必要がある
    return int(datetime.now().timestamp())


class StudentTaskDTO(Base):
    __tablename__ = 'student_tasks'
    id: Union[str, Column] = Column(String(255), primary_key=True, index=True)
    line_user_id: Union[str, Column] = Column(String(255), index=True)
    task: Union[str, Column] = Column(String(255), nullable=False)
    created_at: Union[int, Column] = Column(Integer, index=True, nullable=False)
    updated_at: Union[int, Column] = Column(Integer, index=True, nullable=False)

    def to_entity(self) -> StudentTaskEntity:
        return StudentTaskEntity(
            id=self.id,
            line_user_id=self.line_user_id,
            task=self.task,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @staticmethod
    def from_entity(task: StudentTaskEntity) -> "StudentTaskDTO":
        now = unixTimestamp()
        return StudentTaskDTO(
            id=task.id,
            line_user_id=task.line_user_id,
            task=task.task,
            created_at=now,
            updated_at=now,
        )
