import models
import hashlib
from typing import List, Dict, Any
from datetime import datetime
from fastapi import HTTPException,status
from models import Update_task


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

    def get_tasks(
        self,
    ):
        return self.tasks

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

    

