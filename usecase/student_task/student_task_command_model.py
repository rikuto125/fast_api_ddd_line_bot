from pydantic import BaseModel, Field, validator


class StudentTaskCreateModel(BaseModel):
    """UserCreateModel represents a write model to create a user."""
    id: str = Field(example="id")
    line_user_id: str = Field(example="user_id")
    user_task: str = Field(example="user_name")
    created_at: int = Field(example=1136214245000)
    updated_at: int = Field(example=1136214245000)
