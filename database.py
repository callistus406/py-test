import models
import hashlib
from typing import List, Dict, Any
from datetime import datetime
from fastapi import HTTPException,status
from models import Update_task,Update_comment,Filter_Task,Create_Task

from typing  import Optional


def hash_password(password: str) -> str:
    # print(password.encode(),"encoded")
    return hashlib.sha256(password.encode()).digest()


class Database:
    def __init__(self):
        self.user: List[Dict[str, Any]] = []
        self.tasks: List[Dict[str, Any]] = []
        self.comments: List[Dict[str, Any]] = []
        self.create_static_users()
        self.initialize_tasks()

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
                "username": data["username"],
                "email": data["email"],
                "name": data["name"],
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
    limit: Optional [int] = 20):
        filtered_tasks = []
        if  limit > 30 :
            raise HTTPException(detail="limit cannot exceed 30",status_code=422)
        for task in self.tasks:
            if status is not None and task["status"] != status:
                continue
            if priority is not None and task["priority"] != priority:
                continue
            # if data.start_date is not None and task["start_date"] != data.start_date:
            #     continue
            # if data.end_date is not None and task["end_date"] != data.end_date:
            #     continue


        #  page:limit =
        #     1 :  5  = 4
        #     2 : 5 = 5

            # [page:page]
            # 1 : 1 + 5  = 6 
            # 1:6
            # 2: 2+10  = 12
            
            # 2:12 
        
         

            filtered_tasks.append(task)

        

        if not filtered_tasks:
            raise HTTPException(detail="Task not found", status_code=404)
        return filtered_tasks[page:page+limit]
    
    def get_all_comment(self, ): 
        print(self.comments)
        return self.comments
       
       
    def get_comment(self, id: int):
        for data in self.comments:
            print(data)
            if id == data["comment_id"]:
                return data
        return None
          

    def delete_comment(self, id: int, userId: int, taskId:int):
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
#comment should just be restricted to the owner fo the comment, same applies to deleting



