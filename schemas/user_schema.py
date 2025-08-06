from pydantic import BaseModel

class UserCreate(BaseModel):
    telegram_id: int
    first_name: str
    last_name: str = None
    username: str = None

class UserResponse(BaseModel):
    telegram_id: int
    first_name: str
    last_name: str = None
    username: str = None

    class Config:
        orm_mode = True
