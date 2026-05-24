from  pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

class UserRole(str,Enum):
    ADMIN="admin"
    USER="user"

class Task_Status(str, Enum):
    PENDING="pending"
    ACTIVE="active"
    COMPLETED="completed"

class Task_Priority(str, Enum):
    HIGH="low"
    MEDIUM="medium"
    LOW="low"



class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="The username of the user", )#validat username
    email: str = Field(...,description="The email of the user", ) #todo validate email
    name: str = Field(..., min_length=3, max_length=50, description="The username of the user")
    role: str = UserRole.USER
    password: str= Field(None,min_length=8)
    
class Create_User(UserBase):
    password: str= Field(...,min_length=8)

class Update_User(BaseModel):
    username: str = Field(None, min_length=3, max_length=50, description="The username of the user", )#validat username
    email: str = Field(None,description="The email of the user",) #todo validate email
    name: str = Field(None, min_length=3, max_length=50, description="The username of the user")






class Create_Task(BaseModel):
    title: str = Field(...,min_length=10, max_length=150)
    description:str = Field(...,min_length=10, max_length=500)
    status: Task_Status = Field(default=Task_Status.PENDING)
    priority: Task_Priority = Field(default=Task_Priority.LOW)
    user_id: int = Field(..., description="this is a temporay solution")
    start_date: str
    end_date:str

class Filter_Task(BaseModel):
    search: Optional [str]   = None
    status:Optional [str]  = None
    priority:Optional [str]  = None
    start_date: Optional [str]  = None
    end_date:Optional [str]  = None

class Create_comment(BaseModel):
    comment_id: int
    user_id: int
    task_id: int
    comment: str
    created_at: str
    reply :Optional [str]
class Update_reply(BaseModel):
    content: str
    created_at: Optional  [str]

class Update_task(BaseModel):
    title: Optional [str]   = None
    description:Optional [str]  = None
    status:Optional [str]  = None
    priority:Optional [str]  = None
    start_date: Optional [str]  = None
    end_date:Optional [str]  = None

class Update_comment(BaseModel):
    comment_id:Optional [int]= None
    user_id:Optional [int]= None
    task_id:Optional [int]= None
    comment:Optional [str]= None
    created_at:Optional [str]= None


    # def update_reply(self, id:int, reply_id :int, data: Dict) : 
       
    #     for x in self.comments:
    #         if id == int(x["comment_id"]):
             
    #             for reply in x["replies"]:
    #                 if reply_id == int(reply["id"]):
    #                     print(data["content"])
    #                     reply["content"] = data["content"]
    #                     reply["created_at"] = datetime.now().isoformat(),
    #                     # print(x["replies"])
   
              