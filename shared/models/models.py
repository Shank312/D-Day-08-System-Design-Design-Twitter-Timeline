

from pydantic import BaseModel
from typing import List

class Tweet(BaseModel):
    id: str
    author_id: str
    text: str
    created_at: str
    like_count: int = 0

class Timeline(BaseModel):
    user_id: str
    items: List[Tweet]
