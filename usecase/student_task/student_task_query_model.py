from typing import cast

from pydantic import BaseModel, Field

from domain.student_task.student_task import StudentTaskEntity


class StudentTaskReadModel(BaseModel):
    id: str = Field(example="id")
    line_user_id: str = Field(example="user_id")
    task: str = Field(example="John Doe")
    created_at: int = Field(example=1136214245000)
    updated_at: int = Field(example=1136214245000)

    class Config:
        orm_mode = True

    @staticmethod
    def from_entity(task: StudentTaskEntity) -> "StudentTaskModel":
        return StudentTaskReadModel(
            id=task.id,
            line_user_id=task.line_user_id,
            task=task.task,
            created_at=cast(int, task.created_at),
            updated_at=cast(int, task.updated_at),
        )
