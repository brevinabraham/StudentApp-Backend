from pydantic import BaseModel
from datetime import datetime
import random


class Question(BaseModel):
    user_id: str
    title: str
    content: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    status: str = "open"
    tags: list = []
