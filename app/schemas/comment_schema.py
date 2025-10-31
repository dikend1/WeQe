from pydantic import BaseModel
from .user_schema import UserResponse

class CommentBase(BaseModel):
    content:str


class CommentCreate(CommentBase):
    post_id:int

class CommentUpdate(BaseModel):
    content: str | None = None

class CommentResponse(CommentBase):
    id:int
    post_id:int
    user_id:int
    user: UserResponse | None = None

    class Config:
        from_attributes = True
