from pydantic import BaseModel, Field
from datetime import datetime



class Question(BaseModel):
    user_id: str
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    status_id: list = []
    tags_id: list = []
    topic_id: list = []
    subtopic_id: list = []
    comments_count: int = 0
