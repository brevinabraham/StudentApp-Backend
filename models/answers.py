from pydantic import BaseModel, Field
from datetime import datetime


class Answers(BaseModel):
    question_id: str
    user_id: str
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    like_count: int = 0
    version: int = 0
