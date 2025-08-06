from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[str] = None
    telegram_id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
