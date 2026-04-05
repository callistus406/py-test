from pydantic import BaseModel
from typing import Optional,List
class CreatePost(BaseModel):
    user_id:int
    title: str
    body: str
    
class Comments(BaseModel):
    postId: int
    comment: str
    created_at: str

class UpdatePost(BaseModel):
    user_id:Optional[int] = None
    title: Optional[str] = None
    body: Optional[str] = None
    comments: List[Comments]







class  Item(BaseModel):
    name: str
    description: str
    price: float
    qty: int

