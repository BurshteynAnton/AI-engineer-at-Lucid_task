from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List



class PostBase(BaseModel):
    text: str

class PostCreate(PostBase):
    pass 

class PostUpdate(BaseModel):
    text: Optional[str] = None


class PostInDB(PostBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PostResponse(PostBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PostListResponse(BaseModel):
    posts: List[PostResponse]
    total: int
    cached: bool = False 

class PostCreateResponse(BaseModel):
    postID: int
    message: str = "Post created successfully" 

class PostDeleteResponse(BaseModel):
    message: str = "Post deleted successfully" 
    deleted_post_id: int