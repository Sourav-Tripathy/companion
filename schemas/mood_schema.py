from pydantic import BaseModel
from datetime import datetime

class MoodCreate(BaseModel):
    user_id: int
    mood: str

class MoodResponse(BaseModel):
    user_id: int
    mood: str
    timestamp: datetime

    class Config:
        orm_mode = True
