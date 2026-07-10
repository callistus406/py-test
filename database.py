import models
import bcrypt
from bson import ObjectId
from typing import List, Dict, Any
from datetime import datetime,timezone,timedelta
from fastapi import HTTPException,status
from models import Update_task,Update_comment,Filter_Task,Create_Task,Create_comment,Login_DTO,Login_Response,UserRole,ApiResponse,Create_User
from jose import jwt

from typing  import Optional
from fastapi.responses import JSONResponse
from pymongo import AsyncMongoClient
from utils import logger
SECRET = "ertyuiojhgvbnm"
ALGO = "HS256" 

# database info
MONGO_URL = "mongodb+srv://mack:m6aDKKEFNNVvi5uR@cluster0.kb8caz5.mongodb.net/?appName=Cluster0/task_manger"
DATABASE = "task_manger"
client = None
db = None



async def connect_mongo():
    try:
        global client, db
        client = AsyncMongoClient(MONGO_URL)
        db = client[DATABASE]
        await client.admin.command("ping")
    
        logger.info( "Database Connected successfully")
        # await client.close()
    except Exception as e:
        raise Exception(
            "The following error occurred: ", e)


async def close_mongo_connection():
    
    try:
        if client:
            client.close()
    except Exception as e:
        print(e)

# collections


def hash_password(password: str) -> str:

    # converting password to array of bytes
    bytes = password.encode('utf-8')
    # generating the salt
    salt = bcrypt.gensalt(10)
    # Hashing the password
    return bcrypt.hashpw(bytes, salt)

def validate_password(hashed_password:str,password:str):
    print(hashed_password,password)
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return True
    else:
        return False

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
                "role": "Admin",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            },
        ]

        for user in users:
            self.user.append(user)

    async def create_user(self,user_data: Create_User):
            user_collection = db["users"]

            # check if account exists
            user = await user_collection.find_one({
                "email": user_data.email
            })

            if user is not None:
                raise HTTPException(detail="You can't use this email. Please try another email", status_code=409)
            

            password =  hash_password("password")
            result = await user_collection.insert_one({
                "user_name": user_data.user_name,
                "name": user_data.name,
                "password": password,
                "email": user_data.email,
                "role": UserRole.USER
            })
            return None

        
        

        

    async def  login(self,data: Login_DTO):
        token = None
        user_ = None
        # find the user
        user_collection = db["users"]

        user_ = await user_collection.find_one({
            "email": data.email
        })
        if user_ is None:
            raise HTTPException(detail="Invalid Credential", status_code=401)
            
        
        if validate_password(user_["password"], data.password) is  not True:
              raise HTTPException(detail="Invalid username or Password",status_code=401)
        print("check")
        # generate jwt token
        token = generate_jwt({"sub":str(user_["_id"]),  "role": user_["role"] })
        
        return Login_Response(
            userId=str(user_["_id"]),
            email=user_["email"],
            token=token,
            name=user_["name"],
            role = user_["role"]
        )

    async def get_users(self):
        user_collection = db["users"]
        users = await user_collection.find({}).to_list(length=None)
        for user in users:
            user["_id"] = str(user["_id"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return users

    async def get_user(self, id: str):
        user_collection = db["users"]
        user = await user_collection.find_one({"_id": ObjectId(id)})
        if user:
            user["_id"] = str(user["_id"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def update_user(
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

    async def delete_user(self, id: str):

        user_collection = db["users"]
        user = await user_collection.find_one({"_id": ObjectId(id)})
        print("active")
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        await user_collection.delete_one({"_id": ObjectId(id)})
        if user:
            user["_id"] = str(user["_id"])
        return user
       
          
    async def create_task(self,task: Create_Task,user_id:str ):
        task_collection = db["task"]

        # check if task exists
        is_found = await task_collection.find_one({
            "title": task.title
        })
        
        if is_found is not None:
            raise HTTPException(detail="Duplicate detected", status_code=409)

        payload = {
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
                "start_date": task.start_date,
                "end_date": task.end_date,
                "user_id": ObjectId(user_id),
                "completed_at": None,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
        }
        result =  await task_collection.insert_one(payload)
        return None

        
  
  
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

  
    async def get_task(self, id: int,):
        task_collection = db["task"]
        task = await task_collection.find_one({"_id": ObjectId(id)})
        if task:
            task["_id"] = str(task["_id"])
        if not task:
            raise HTTPException(status_code=404, detail="User not found")
        return task
        

    async def delete_task(self, id: str,user_ID:int, role:str):
        print("check")
        task_collection = db["task"]
        task = await task_collection.find_one({"_id": ObjectId(id)})
        print(task)
        temp = []

        print(role)
        print(task["user_id"])
        print(type(task["user_id"]), type(int(user_ID)))
        print(role == UserRole.ADMIN)
        
        if  task:   
            if  task["user_id"] != int(user_ID) and role != UserRole.ADMIN:
                print("check")
                raise HTTPException(detail="you are not authorized to delete this Task", status_code=403)
            else:
                await task_collection.delete_one({"_id": ObjectId(id)})
                if task:
                    task["_id"] = str(task["_id"])
                return task
        else:
                raise HTTPException(detail="Task not found", status_code=403)

    def update_task_(self,id:int,data:Update_task, role, user_id):
        is_TaskFound = False
        isRoleOwner = False
        response = None
        print(type(user_id))
        for task in self.tasks:
            
            if (id == task["id"] ):
                is_TaskFound = True
               
                print(type( task["user_id"]))
                print( user_id == task["user_id"])
                if (role == UserRole.ADMIN ) or  int(user_id) ==task["user_id"]:
                    isRoleOwner = True
                    print(user_id, task["user_id"] )
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
                    print("finished")
        if is_TaskFound == False :
                 print("Accees1")  
                 raise HTTPException(detail="Task not found",status_code=404) 
              
        if isRoleOwner ==False:
                print("Accees2")
                raise HTTPException(detail="Unauthorize access, only admin and owners can update task",status_code=404)
                
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
            "tasks" : filtered_tasks[start:end],
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
                    "content": "approved",
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


    async def create_comment(self):
        if len(self.comments) ==0:
            last_id = 1
        else:
            last_comments = self.comments[-1]
            last_id = self.genId(last_comments["id"])
            comment_collection = db["comments"]
            result =  await comment_collection.insert_many([{
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
                    "content": "approved",
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
            }])
    async def get_all_comment(self,): 
        comment_collection = db["tasks"]
        comment = await comment_collection.find({}).to_list(length=None)
        if comment:
            comment["_id"] = str(comment["_id"])
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        return comment
       
       
    async def get_comment(self, id: int):
        comment_collection = db["tasks"]
        comment = await comment_collection.find_one({"_id": ObjectId(id)})
        if comment:
            comment["_id"] = str(comment["_id"])
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        return comment
    
    def update_reply(self, id:int, reply_id :int, data: Dict) : 
       
        for x in self.comments:
            if id == int(x["comment_id"]):
             
                for reply in x["replies"]:
                    if reply_id == int(reply["id"]):
                        print(data["content"])
                        reply["content"] = data["content"]
                        reply["created_at"] = datetime.now().isoformat(),
                        # print(x["replies"])
   
              
          

    async def delete_comment(self, id:int, taskId:int, user_ID:int):
        # for x,data in enumerate(self.comments):
        #     print(x,data)
        #     if id == data["comment_id"] and user_id == data["user_id"] and taskId == data["task_id"]:
        #         print(data["comment_id"] )
        #         # print(self.comments.data[id])
        #         self.comments.pop(x)        
        # return None
        comment_collection = db["comment"]
        comment = await comment_collection.find_one({"_id": ObjectId(id)})
        print(comment)
        temp = []

        print(role)
        print(comment["user_id"])
        print(type(task["user_id"]), type(int(user_ID)))
        
        if  comment:   
            if  comment["user_id"] != int(user_ID):
                print("check")
                raise HTTPException(detail="you are not authorized to delete this Task", status_code=403)
            else:
                await comment_collection.delete_one({"_id": ObjectId(id)})
                if comment:
                    comment["_id"] = str(comment["_id"])
                return comment
        else:
                raise HTTPException(detail="Task not found", status_code=403)
    
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



