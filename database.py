import models
import bcrypt
from bson import ObjectId
from typing import List, Dict, Any
from datetime import datetime,timezone,timedelta
from fastapi import HTTPException,status
from models import Update_task,Update_comment,Filter_Task,Create_Task,Create_comment,Login_DTO,Login_Response,UserRole,ApiResponse,Create_User,Update_User
from jose import jwt

from typing  import Optional
from fastapi.responses import JSONResponse
from pymongo import AsyncMongoClient
from utils import logger
SECRET = "ertyuiojhgvbnm"
ALGO = "HS256" 

# database info
MONGO_URL = "mongodb+srv://neme_python:test123@info-3139.fvv8kuz.mongodb.net/?appName=INFO-3139/task_manger"

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
              # check if account username exists
            user = await user_collection.find_one({
                "user_name": user_data.user_name
            })

            if user is not None:
                raise HTTPException(detail="You can't use this username. Please try another username", status_code=409)

            password =  hash_password("password")
            result = await user_collection.insert_one({
                "user_name": user_data.user_name,
                "name": user_data.name,
                "password": password, #Q hare are we returning this as hashed in the userResponse?
                "email": user_data.email,
                "role": UserRole.USER
            })
            print(user)
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
        users = await user_collection.find({},{"password":0}).to_list(length=None)
        for user in users:
            user["_id"] = str(user["_id"])
        if not users:
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

    async def update_user(self, user_data: Update_User, user_id: str):
        print(user_data)
        user_collection = db["users"]

        # Check whether the user exists
        user = await user_collection.find_one(
            {"_id": ObjectId(user_id)}
        )

        if user is None:
            raise HTTPException(
                detail="User not found",
                status_code=409
            )

        # Check whether another user already has this email
        existing_email = await user_collection.find_one({
            "email": user_data.email, "_id": {"$ne": ObjectId(user_id)}
        })
        print(existing_email)
        print(user_data.email)
        if existing_email is not None:
            raise HTTPException(
                detail="You can't use this email. Please try another email",
                status_code=409
            )

        # Check whether another user already has this username
        existing_username = await user_collection.find_one({
            "user_name": user_data.user_name, "_id": {"$ne": ObjectId(user_id)}
        })

        if existing_username is not None:
            raise HTTPException(
                detail="You can't use this username. Please try another username",
                status_code=409
            )

        #neglects null fields
        update_data = user_data.model_dump(exclude_none=True)
        await user_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
      
        updated_user = await user_collection.find_one(
       {"_id": ObjectId(user_id)},{"password":0}
        )
      
        updated_user["_id"] = str(updated_user["_id"])
        return updated_user



    async def delete_user(self, id: str):

        user_collection = db["users"]
        user = await user_collection.find_one({"_id": ObjectId(id)})
        print("active")
       
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if  user["role"] != UserRole.ADMIN:
                print("check")

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

        
  
  
    

  
    async def get_task(self, id: int,):
        task_collection = db["task"]
        task = await task_collection.find_one({"_id": ObjectId(id)})
        if task:
            task["_id"] = str(task["_id"])
        if not task:
            raise HTTPException(status_code=404, detail="User not found")
        return task
        

    async def delete_task(self, id: str,user_ID:str, role:str):
        print("check")
        task_collection = db["task"]
        task = await task_collection.find_one({"_id": ObjectId(id)})
        print(task)
        
        if  task:   
            if  task["user_id"] != (user_ID) and role != UserRole.ADMIN.value:
                print("check")
                raise HTTPException(detail="you are not authorized to delete this Task", status_code=403)
            else:
                await task_collection.delete_one({"_id": ObjectId(id)})
                if task:
                    task["_id"] = str(task["_id"])
                return task
        else:
                raise HTTPException(detail="Task not found", status_code=403)

    async def update_task_(self,id:str,data:Update_task, role, user_id:str):
        task_collection = db["task"]
        task = await task_collection.find_one({"_id": ObjectId(id)})
        print(task)

    
        print(type(role))
        print((UserRole.ADMIN.value))
        print(user_id)
       
       
        print(task["user_id"] != ObjectId(user_id))
        print( role != UserRole.ADMIN.value)
        if  task:   
            if  task["user_id"] != ObjectId(user_id) and role != UserRole.ADMIN.value:
                print("check")
                raise HTTPException(detail="you are not authorized to update this Task", status_code=403)
            
            else:
                    
                    # Check whether another task already has this title
                    existing_taskname = await task_collection.find_one({
                        "title": data.title, "_id": {"$ne": ObjectId(id)}
                    })
                
                    if existing_taskname is not None:
                        raise HTTPException(
                            detail="You can't use this TASK NAME. Please try another name",
                            status_code=409
                        )
                
                    #neglects null fields
                    update_data = data.model_dump(exclude_none=True)
                    await task_collection.update_one(
                        {"_id": ObjectId(id)},
                        {"$set": update_data}
                    )
                
                    updated_task = await task_collection.find_one(
                {"_id": ObjectId(id)},{"password":0}
                    )
                    print(updated_task)
                    updated_task["_id"] = str(updated_task["_id"])
                    updated_task["user_id"] = str(updated_task["user_id"])
                    return updated_task
        else:
             raise HTTPException(
                detail="Task not found",
                status_code=409
            )
 
    def initialize_comment(self):
    
        # Sample datasets for Create_comment
        SAMPLE_COMMENTS: List[dict] = [

       
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


    async def create_comment(self, data:Create_comment, usersId:str, taskId:str):
        print("active")
        comment_collection = db["comments"]
        exist = await comment_collection.find_one({ "comment": data.comment })
        if exist is not None:
            raise HTTPException(detail="Duplicate detected", status_code=409)
        # user_collection = db["users"]
        # task_collection = db["tasks"]
        payload = {
            "user_id": ObjectId(usersId),
            "task_id":ObjectId(taskId),
            "comment": data.comment,
            "create_at": datetime.now().isoformat(),
            "replies": []
        }
        result = await comment_collection.insert_one(payload)
        

        return None
    async def get_all_comment(self,): 
        comment_collection = db["comments"]
        comments = await comment_collection.find({}).to_list(length=None)
        for comment in comments:
            comment["_id"] = str(comment["_id"])
            comment["user_id"] = str(comment["user_id"])
            comment["task_id"] = str(comment["task_id"])
        
        if not comments:
            raise HTTPException(status_code=404, detail="Comment not found")
        return comments
       
       
    async def get_comment(self, str: int):
        comment_collection = db["comments"]
        comment = await comment_collection.find_one({"_id": ObjectId(id)})
        if comment:
            comment["_id"] = str(comment["_id"])
            comment["user_id"] = str(comment["user_id"])
            comment["task_id"] = str(comment["task_id"])
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        return comment
    
    # async def update_reply(self, id:int, reply_id :int, data: Dict) :    
      
   
              
          

    async def delete_comment(self, id:str, user_ID:str, role:str):     
        comment_collection = db["comments"]
        comments = await comment_collection.find_one({"_id": ObjectId(id)})
        print(comments)
        temp = []

        print(role)
        print(comments["user_id"])
        
        
        if  comments:   
            if  comments["user_id"] != (user_ID) and role != UserRole.ADMIN:
                print("check")
                raise HTTPException(detail="you are not authorized to delete this Task", status_code=403)
            else:
                await comment_collection.delete_one({"_id": ObjectId(id)})
                if comments:
                    comments["_id"] = str(comments["_id"])
                    comments["user_id"] = str(comments["user_id"])
                    comments["task_id"] = str(comments["task_id"])
                return comments
        else:
                raise HTTPException(detail="Task not found", status_code=403)
    
    async def update_comment(self,id:str, data:Update_comment,user_id:str):
        comment_collection = db["task"]
        comment = await comment_collection.find_one({"_id": ObjectId(id)})
        print(comment)
       

        if  comment:   
            if  comment["user_id"] != ObjectId(user_id) :
                print("check")
                raise HTTPException(detail="you are not authorized to update this Comment", status_code=403)
            else:
                    #neglects null fields
                    update_data = data.model_dump(exclude_none=True)
                    await comment_collection.update_one(
                        {"_id": ObjectId(id)},
                        {"$set": update_data}
                    )
                
                    updated_comment = await comment_collection.find_one(
                {"_id": ObjectId(id)},{"password":0}
                    )
                    updated_comment["_id"] = str(updated_comment["_id"])
                    updated_comment["user_id"] = str(updated_comment["user_id"])
                    updated_comment["task_id"] = str(updated_comment["task_id"])
                    return updated_comment
        else:
             raise HTTPException(
                detail="Comment not found",
                status_code=409
            )

    #  def createComment()   

#comment should just be restricted to the owner fo the comment, same applies to deleting



