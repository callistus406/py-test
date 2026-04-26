from  pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

class UserRole(str,Enum):
    ADMIN="admin"
    USER="user"


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="The username of the user", examples="user@123")#validat username
    email: str = Field(...,description="The email of the user", example= "user@gmail.com") #todo validate email
    name: str = Field(..., min_length=3, max_length=50, description="The username of the user")
    role: str = UserRole.USER
    password: str= Field(None,min_length=8)
    
class Create_User(UserBase):
    password: str= Field(...,min_length=8)

class Update_User(BaseModel):
    username: str = Field(None, min_length=3, max_length=50, description="The username of the user", examples="user@123")#validat username
    email: str = Field(None,description="The email of the user", example= "user@gmail.com") #todo validate email
    name: str = Field(None, min_length=3, max_length=50, description="The username of the user")






class Create_task(BaseModel):
    title:Optional [str]
    description:str
    status:str
    priority:str
    start_date: str
    end_date:str

class Creare_comment(BaseModel):
    task_id: int
    user_id: int
    comment: str
    create_at: str

class Update_task(BaseModel):
    title: Optional [str]   = None
    description:Optional [str]  = None
    status:Optional [str]  = None
    priority:Optional [str]  = None
    start_date: Optional [str]  = None
    end_date:Optional [str]  = None
