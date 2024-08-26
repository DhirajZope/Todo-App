from typing import Optional
from pydantic import BaseModel, Field


class TodoRequest(BaseModel):
    title: str = Field(min_length=1, max_length=128)
    description: Optional[str] = Field(description="This field is optional.", default=None)
    priority: int = Field(default=1, lt=5, gt=0)
    completed: bool = Field(default=False)
