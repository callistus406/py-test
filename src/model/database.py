import schema.schema as schema
import bcrypt
from bson import ObjectId
from typing import List, Dict, Any
from datetime import datetime,timezone,timedelta
from fastapi import HTTPException,status
from schema.schema import Update_task,Update_comment,Filter_Task,Create_Task,Create_comment,Login_DTO,Login_Response,UserRole,ApiResponse,Create_User,Update_User
from jose import jwt
from dotenv import load_dotenv
import os

from typing  import Optional
from fastapi.responses import JSONResponse
from pymongo import AsyncMongoClient
from utils import logging

load_dotenv()
# database info
MONGO_URL= os.getenv("MONGO_URL")
SECRET = os.getenv("JWT_SECRET")
ALGO = os.getenv("JWT_ALGO") 

DATABASE = "task_manger"
client = None
db = None




async def connect_mongo():
    try:
        global client, db
        client = AsyncMongoClient(MONGO_URL)
        db = client[DATABASE]
        await client.admin.command("ping")
    
        logging.logger.info( "Database Connected successfully")
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
        task_collection = db["task"]
        task = await task_collection.find_one({"_id": ObjectId(id)})
        
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
        if  comments:   
            if  comments["user_id"] != (user_ID) and role != UserRole.ADMIN:
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
