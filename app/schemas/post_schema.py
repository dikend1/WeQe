from pydantic import BaseModel
from .user_schema import UserResponse

class PostBase(BaseModel):
    title:str
    content:str

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id:int
    owner_id: int
    owner: UserResponse | None = None

    class Config:
        from_attributes = True
