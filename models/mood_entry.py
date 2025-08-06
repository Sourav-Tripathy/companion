from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MoodEntry(BaseModel):
    id: Optional[str] = None
    user_id: int
    mood: str
    timestamp: datetime = datetime.now()
