import models
import hashlib
from typing import List, Dict, Any
from datetime import datetime,timezone,timedelta
from fastapi import HTTPException,status
from models import Update_task,Update_comment,Filter_Task,Create_Task,Create_comment,Login_DTO
from jose import jwt

from typing  import Optional

SECRET = "ertyuiojhgvbnm"
ALGO = "HS256" 

def hash_password(password: str) -> str:
    # print(password.encode(),"encoded")
    return hashlib.sha256(password.encode()).digest()



def validate_password(plain_password:str, hashed_password:str):
    hash1 = hashed_password
    hash2 =  hash_password(plain_password)
    return hash1 == hash2


def generate_jwt(data:Dict, exp:int = 30):
    to_encode = data.copy()
    conv_time = datetime.now(timezone.utc) + timedelta(minutes=exp)

    to_encode.update({
        exp:conv_time
    })
    # ?generate token
    return jwt.encode(
        data,
        SECRET,
        algorithm=ALGO

    )



class Database:
    def __init__(self):
        self.user: List[Dict[str, Any]] = []
        self.tasks: List[Dict[str, Any]] = []
        self.comments: List[Dict[str, Any]] = []
        self.create_static_users()
        self.initialize_tasks()
        self.initialize_comment()

    def genId(self, lastId: int):
        return lastId + 1

    def create_static_users(self):
        users = [
            {
                "id": 1,
                "user_name": "Kelly",
                "email": "key@gmail.com",
                "name": "kelly joe",
                "is_active": True,
                "password": hash_password("password"),
                "role": "user",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            },
            {
                "id": 2,
                "user_name": "kenneth",
                "email": "kenet@gmail.com",
                "name": "kennet bully",
                "is_active": True,
                "password": hash_password("password"),
                "role": "user",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            },
            {
                "id": 3,
                "user_name": "hailey",
                "email": "hailey@gmail.com",
                "name": "hailey kent",
                "is_active": True,
                "password": hash_password("password"),
                "role": "user",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            },
        ]

        for user in users:
            self.user.append(user)


    def  login(self,data: Login_DTO):
        token = None
        # get user
        for user in self.user:
            print(user["email"].lower() , data.email.lower())
            if user["email"].lower() == data.email.lower():
                if validate_password(data.password,user["password"]):
                    # generate jwt token
                    token =   generate_jwt({
                            "sub":1243,
                        })
                    print(token)
                else:
                    raise HTTPException(status_code=401, detail="Invalid Email Or Password")
        # else:
        #     raise HTTPException(status_code=401, detail="Invalid credentials")

        return token
        #  
        # get the password

        # march password with stored password
        # pass



    def create_user(self, user: models.UserBase):
        data = user.model_dump()
        #    find the last user in the db
        last_id = None
        if len(self.user) == 0:
            last_id = 1
        else:
            last_user = self.user[-1]
            last_id = self.genId(last_user["id"])
            print(last_id)
        self.user.append(
            {
                "id": last_id,
                "user_name": data["user_name"],
                "email": data["email"],
                "name": data["name"],
                "is_active": True,
                "password": hash_password(data["password"]),
                "updated_at" : datetime.now().isoformat(),
                "created_at" : datetime.now().isoformat(),

            }
        )
        print(self.user)

    def get_users(self):
        users = []
        for user in self.user:
            del user["password"]
            users.append(user)
        return users

    def get_user(self, id: int):
        for user in self.user:
            if user["id"] == id:
                del user["password"]
                return user

    def update_user(
        self, id: int, username: str, name: str, email: str, isactive: bool, role: str
    ):
        for data in self.user:
            if self.user["id"] == id:
                self.user["id"] = id
                self.user["username"] = username
                self.user["name"] = name
                self.user["email"] = email
                self.user["isactive"] = isactive
                self.user["role"] = role
                self.user["updated_at"] = datetime.now().isoformat()

    def delete_user(self, id: int):
        for data in self.user:
            del self.user[id]



    # tasks

    def initialize_tasks(self):
# data_main[0]["title"]
        data_main = [
            {
                "title": "Build login API",
                "description": "Develop and test authentication endpoints",
                "status": "active",
                "priority": "high",
                "start_date": "2026-04-01",
                "end_date": "2026-04-07",
                "user_id": 1,
                "created_by": 1,
                "updated_by": 2,
                "completed_at": None,
                "id": 1,
                "created_at": datetime.now().isoformat(), 
                "updated_at": datetime.now().isoformat(),
            },
            {
                "title": "Design database schema",
                "description": "Create ER diagram and define relationships",
                "status": "completed",
                "priority": "high",
                "start_date": "2026-03-20",
                "end_date": "2026-03-25",
                "user_id": 2,
                "created_by": 1,
                "updated_by": 2,
                "completed_at": "2026-03-25",
                "id": 2,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            },
            {
                "title": "Write unit tests",
                "description": "Add tests for service layer functions",
                "status": "pending",
                "priority": "medium",
                "start_date": "2026-04-10",
                "end_date": "2026-04-15",
                "user_id": 3,
                "created_by": 2,
                "updated_by": 2,
                "completed_at": None,
                "id": 3,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            },
            {
                "title": "Frontend UI updates",
                "description": "Improve dashboard layout and responsiveness",
                "status": "active",
                "priority": "medium",
                "start_date": "2026-04-02",
                "end_date": "2026-04-12",
                "user_id": 4,
                "created_by": 3,
                "updated_by": 4,
                "completed_at": None,
                "id": 4,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            },
            {
                "title": "Deploy to production",
                "description": "Push latest release and monitor logs",
                "status": "pending",
                "priority": "low",
                "start_date": "2026-04-20",
                "end_date": "2026-04-21",
                "user_id": 5,
                "created_by": 1,
                "updated_by": 1,
                "completed_at": None,
                "id": 5,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            },
            
        ]

        for task in data_main:
            self.tasks.append(task)

    def create_task(self,task:Create_Task):
        data = task.model_dump()
        new_task_id = self.tasks[-1]["id"]+1
        data["id"] = new_task_id
        data["created_at"] =  datetime.now().isoformat()
        data["updated_at"] = datetime.now().isoformat()
        data["user_id"] =  task.user_id
        data["created_by"] = task.user_id
        self.tasks.append(data)
        return self.tasks[-1]

  
  
  
    def create_comment(self, data:Create_comment):
        newSet = data.model_dump()
        lastIndex = self.comments[-1]["comment_id"]
        startingIndex = lastIndex + 1
        newSet["comment_id"] = startingIndex
        newSet["comment"] = data.comment
        newSet["task_id"] = data.task_id 
        newSet["created_at"] = datetime.now()
        newSet["user_id"] = data.user_id 

        self.comments.append(newSet)
        return self.comments[-1]




  
  
    def get_task(self, id: int, status: str):
        for data in self.tasks:
            print(data)
            if id == data["id"]:
                return data
            return None

    def delete_task(self, id: int):
        for data in self.tasks:
            if id == data[id]:
                del self.tasks["id"]
        return None

    def update_task_(self,id:int,data:Update_task):

        is_found = False
        response = None
        for task in self.tasks:
            
            if id == task["id"]:
                is_found = True
                
                if data.title is not None:
                    task["title"] = data.title
                if data.description is not None:
                    task["description"] = data.description
                if data.status is not None:
                    task["status"] = data.status
                if data.priority is not None:
                    task["priority"] = data.priority
                if data.start_date is not None:
                    task["start_date"] = data.start_date
                if data.end_date is not None:
                    task["end_date"] = data.end_date
                task["updated_at"] = datetime.now().isoformat(),
                response = task


        if is_found is not True:
            raise HTTPException(detail="Task not found",status_code=404)    
        return response

    def filter_task_(self, status: Optional [str] = None,priority: Optional [str] = None,   
    page: Optional [int]  =1 ,
    limit: Optional [int] = 20, search: Optional[str] = None ):
        filtered_tasks = []
        print(search)
       
        if   limit > 30 :
            raise HTTPException(detail="limit cannot exceed 30",status_code=422)
        for task in self.tasks:
         
            if status is not None and task["status"] != status:
                continue
            if priority is not None and task["priority"] != priority:
                continue
            if search is not None:
               
                searchLower = search.lower()
                titleMatch = searchLower in task["title"].lower()
                descriptionMatch = searchLower in task["description"].lower()
                
                if not (titleMatch or descriptionMatch):
                    continue

            print(task)        
            filtered_tasks.append(task)

        

        if not filtered_tasks:
            raise HTTPException(detail="Task not found", status_code=404)
        
        print(filtered_tasks[page:page+limit])
        print(page, limit)
       
        # if page is not None and 
        # return filtered_tasks[page:page+limit]
      
        start = (page - 1) * limit
        end = start + limit
        return {
            "data" : filtered_tasks[start:end],
            "metadata" : 
            {
                "record": len(filtered_tasks),
                "total" : len(self.tasks),
            }
        }
    
    def initialize_comment(self):
    
        # Sample datasets for Create_comment
        SAMPLE_COMMENTS: List[dict] = [

        {
            "comment_id": 1,
            "user_id": 2,
            "task_id":1,
            "comment": "Please update the documentation.",
            "create_at": datetime.now().isoformat(),
        },
        {
            "comment_id": 2,
            "user_id": 2,
            "task_id":1,
            "comment": "Found a bug in edge case handling.",
            "create_at": datetime.now().isoformat(),
        },
        {
            "comment_id": 3,
            "user_id": 11,
            "task_id":2,
            "comment": "Ready for QA.",
            "create_at": datetime.now().isoformat(),
        },
        {
            "comment_id": 4,
            "user_id": 1,
            "task_id":3,
            "comment": "Deployed to staging.",
            "create_at": datetime.now().isoformat(),
        },
        {
            "comment_id": 5,
            "user_id": 1,
            "task_id":3,
            "comment": "Needs performance benchmarking.",
            "create_at": datetime.now().isoformat(),
        },
        {
            "comment_id": 6,
            "task_id": 1,
            "user_id": 2,
            "comment": "this is from the admin",
            "created_at": "2026-05-17T10:00:00",
            "replies": [
                {
                    "id": 1,
                    "userId": 3,
                    "content": "this is a reply from the user",
                    "created_at": "2026-05-17T10:01:00"
                }
            ]
        },
        {
            "comment_id": 7,
            "task_id": 1,
            "user_id": 4,
            "comment": "please review the task updates",
            "created_at": "2026-05-17T10:02:00",
            "replies": [
                {
                    "id": 1,
                    "userId": 5,
                    "content": "looks good to me",
                    "created_at": "2026-05-17T10:03:00"
                },
                {
                    "id": 2,
                    "userId": 6,
                    "content": "approved 👍",
                    "created_at": "2026-05-17T10:04:00"
                }
            ]
        },
        {
            "comment_id": 8,
            "task_id": 2,
            "user_id": 7,
            "comment": "can someone check this task?",
            "created_at": "2026-05-17T10:05:00",
            "replies": []
        },
        {
            "comment_id": 9,
            "task_id": 2,
            "user_id": 8,
            "comment": "UI needs improvement",
            "created_at": "2026-05-17T10:06:00",
            "replies": [
                {
                    "id": 1,
                    "userId": 9,
                    "content": "agree, spacing is off",
                    "created_at": "2026-05-17T10:07:00"
                }
            ]
        },
        {
            "comment_id": 10,
            "task_id": 3,
            "user_id": 1,
            "comment": "deployment is ready",
            "created_at": "2026-05-17T10:08:00",
            "replies": [
                {
                    "id": 1,
                    "userId": 2,
                    "content": "tested on staging, all good",
                    "created_at": "2026-05-17T10:09:00"
                }
            ]
        },
        {
            "comment_id": 11,
            "task_id": 3,
            "user_id": 3,
            "content": "database migration completed",
            "created_at": "2026-05-17T10:10:00",
            "replies": []
        },
        {
            "comment_id": 12,
            "task_id": 4,
            "user_id": 5,
            "comment": "API response is slow",
            "created_at": "2026-05-17T10:11:00",
            "replies": [
                {
                    "id": 1,
                    "user": 6,
                    "content": "we should optimize queries",
                    "created_at": "2026-05-17T10:12:00"
                },
                {
                    "id": 2,
                    "userId": 7,
                    "content": "adding index might help",
                    "created_at": "2026-05-17T10:13:00"
                }
            ]
        },
        {
            "comment_id": 13,
            "task_id": 4,
            "user_id": 8,
            "comment": "authentication bug found",
            "created_at": "2026-05-17T10:14:00",
            "replies": [
                {
                    "id": 1,
                    "userId": 9,
                    "content": "I can reproduce it",
                    "created_at": "2026-05-17T10:15:00"
                }
            ]
        },
        {
            "comment_id": 14,
            "task_id": 3,
            "user_id": 3,
            "comment": "need clarification on requirements",
            "created_at": "2026-05-17T10:16:00",
            "replies": []
        },
        {
            "comment_id": 15,
            "task_id": 3,
            "user_id": 10,
            "comment": "final review completed",
            "created_at": "2026-05-17T10:17:00",
            "replies": [
                {
                    "id": 1,
                    "userId": 1,
                    "content": "great work everyone",
                    "created_at": "2026-05-17T10:18:00"
                }
            ]
        }
    ]
    
        for x in SAMPLE_COMMENTS:
            self.comments.append(x)

    def get_all_comment(self,  ): 
        print(self.comments)
        return self.comments
       
       
    def get_comment(self, id: int):
        list =[]
        for data in self.comments:
            if id ==data["task_id"]:
                print(data)
                list.append(data)
        return list
    
    def update_reply(self, id:int, reply_id :int, data: Dict) : 
       
        for x in self.comments:
            if id == int(x["comment_id"]):
             
                for reply in x["replies"]:
                    if reply_id == int(reply["id"]):
                        print(data["content"])
                        reply["content"] = data["content"]
                        reply["created_at"] = datetime.now().isoformat(),
                        # print(x["replies"])
   
              
          

    def delete_comment(self, id: int,userId: int, taskId:int):
        for x,data in enumerate(self.comments):
            print(x,data)
            if id == data["comment_id"] and userId == data["user_id"] and taskId == data["task_id"]:
                print(data["comment_id"] )
                # print(self.comments.data[id])
                self.comments.pop(x)
                
                
        return None
    
    def update_comment(self,id:int, data:Update_comment):
        is_found = False
        response = None
        for com in self.comments:
            
            if id == com["comment_id"]:
                is_found = True
                com["comment"] = data.comment
                com["created_at"] = datetime.now().isoformat(),
                response = com
        if is_found is not True:
            raise HTTPException(detail="Comment not found",status_code=404)    
        return response


    #  def createComment()   

#comment should just be restricted to the owner fo the comment, same applies to deleting



