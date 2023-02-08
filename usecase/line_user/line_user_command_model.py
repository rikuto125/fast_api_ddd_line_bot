from pydantic import BaseModel, Field, validator


class LineUserCreateModel(BaseModel):
    """UserCreateModel represents a write model to create a user."""
    line_user_id: str = Field(example="user_id")
    user_name: str = Field(example="user_name")
    created_at: int = Field(example=1136214245000)
    updated_at: int = Field(example=1136214245000)
