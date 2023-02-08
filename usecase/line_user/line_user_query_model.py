from typing import cast

from pydantic import BaseModel, Field

from domain.line_user.line_user import LineUserEntity


class LineUserReadModel(BaseModel):
    line_user_id: str = Field(example=1)
    name: str = Field(example="John Doe")
    created_at: int = Field(example=1136214245000)
    updated_at: int = Field(example=1136214245000)

    class Config:
        orm_mode = True

    @staticmethod
    def from_entity(user: LineUserEntity) -> "UserReadModel":
        return LineUserReadModel(
            line_user_id=user.line_user_id,
            name=user.user_name,
            created_at=cast(int, user.created_at),
            updated_at=cast(int, user.updated_at),
        )
