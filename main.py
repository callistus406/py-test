
from fastapi import FastAPI, Request, Query, status, HTTPException,Body,Depends
import json
from models import Create_User, Filter_Task,Update_task, Update_comment,Update_reply, Create_Task, Create_comment,Login_DTO,Login_Response,UserRole, ApiResponse,Get_Task_Response
import database
from typing  import Optional,Dict, TypeVar
from fastapi.responses import JSONResponse
import logging
from middleware import validate_token,validate_admin,require_role

app = FastAPI()

db = database.Database()




# connet db

@app.on_event("startup")
async def startup_event():
    await database.connect_mongo()

# @app.on_event("shortdown")
# async def startup_event():
#    await  database.close_mongo_connection()
   

#does this exception handle all task endpoint failure?
@app.exception_handler(HTTPException)
async def http_exception_handler(request:Request,exc:HTTPException):
    # logger.error("... Running exception interceptor")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "data": []
        }
    )

# ========================|| Authentication endpoints ||====================================

@app.post("/login", response_model=ApiResponse[Login_Response],status_code=status.HTTP_200_OK )
async def login(user: Login_DTO):
    
    return {"success": True,
    "message": "All users retrieved successfully",
    "data":await db.login(user)}


@app.post("/register", status_code=status.HTTP_201_CREATED,response_model=ApiResponse  )
async def register(user_data:Create_User):
    response  = await db.create_user(user_data)
    return {"success": True,
    "message": "User Created Successfully",
    "data": response}


# ========================|| User endpoints ||====================================

@app.get("/users", status_code=status.HTTP_200_OK,response_model=ApiResponse)
# def getUsers(user=Depends(require_role([UserRole.ADMIN]))):
async def getUsers():
    # print(user)
    response = await db.get_users()
    return {  
        "success":True,
        "message": "Successfully Fetched All Users",
        "data":response 
    }

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK,response_model=ApiResponse)
async def get_user_by_id(user_id: str):
    return {  
        "success":True,
        "message": "Successfully Fetched User",
        "data": await db.get_user(user_id)}

@app.delete("/users/{user_id}", status_code=status.HTTP_200_OK,response_model=ApiResponse)
async def get_user_by_id(user_id: str):
    return {  
        "success":True,
        "message": "Successfully Deleted User",
        "data": await db.delete_user(user_id)}

# ========================|| Task endpoints ||====================================

@app.post("/tasks", status_code=status.HTTP_200_OK,response_model=ApiResponse[Get_Task_Response] )
async def create_task(data:Create_Task, user=Depends(validate_token)):
    user_id  = user["user_id"]
    response = await db.create_task(data, user_id)
    return  {
        "success":True,
        "message": "Request Successful",
        "data": response
    }

@app.delete("/tasks/{id}", status_code=status.HTTP_200_OK,response_model=ApiResponse)
async def delete_task(id:str,user=Depends(require_role([UserRole.USER,UserRole.ADMIN]))):
    print("test")
    user_id = user["user_id"]
    role = user["role"]
    print(role, user_id)
    return { 
        "success":True,
        "message": "Successfully deleted field",
        "data": await db.delete_task(id, user_id,role)}





# filter endpoint
@app.get("/tasks", status_code=status.HTTP_200_OK, response_model=ApiResponse[Get_Task_Response])
async def filter_tasks(
    status: Optional [str] = None,
    priority: Optional [str] = None,
    page: Optional [int] = 1,
    limit: Optional [int] =20,
    search: Optional [str]= Query(None),   
):
    return {
        "success":True,
        "message": "Request Successful - getting all task with the desired filter",
        "data":  await db.filter_task_(status,priority,page,limit,search)}


@app.get("/tasks/{task_id}", status_code=status.HTTP_200_OK,response_model=ApiResponse[Get_Task_Response])
async def get_task(task_id: str):
    response = await db.get_task(task_id)
    return  {
        "success":True,
        "message": "Request Successful",
        "data": response
    }


@app.put("/tasks/{task_id}", status_code=status.HTTP_200_OK,response_model=ApiResponse)
async def update_task(task_id,body:Update_task,user=Depends(require_role([UserRole.USER,UserRole.ADMIN]))):

    role = user["role"]  
    user_id = user["user_id"]
    response= await  db.update_task_(int(task_id), body, role, user_id)
    return  {
        "success":True,
        "message": "Request Successful - fetched task by ID",
        "data": response
    }

# ========================|| Comment endpoints ||====================================

@app.get("/comments", status_code=status.HTTP_200_OK,response_model=ApiResponse)
def get_all_comment():
    return {
        "success":True,
        "message": "Request Successful Retrieved All Comments",
        "data": db.get_all_comment()}

@app.post("/create_commment", status_code = status.HTTP_200_OK,response_model=ApiResponse)
async def create_comment(data:Create_comment,user=Depends(require_role([UserRole.USER,UserRole.ADMIN]))):
    user_id = user["user_id"]
    return{
        "success":True,
        "message": "Request Successful Created a Comment",
        "data": await db.create_comment(data)}

@app.get("/comments/{comment_id}", status_code=status.HTTP_200_OK,response_model=ApiResponse)
async def get_comment(comment_id):
    return {
        "success":True,
        "message": "Request Successful Fetched Comment by ID",
        "data":await  db.get_comment(int(comment_id))}

@app.delete("/comments/{comment_id}/x{task_id}", status_code=status.HTTP_200_OK,response_model=ApiResponse)
def delete_comment(comment_id,user_id,task_id, user= Depends(validate_token)):
   user_id = user["user_id"]
   return {
        "success":True,
        "message": "Request Successful Deleted Comment by ID",
       "data": db.delete_comment(int(comment_id),int(user_id),int(task_id))}

@app.put("/comments/{comment_id}/{reply_id}", status_code=status.HTTP_200_OK,response_model=ApiResponse)
def update_reply(comment_id, reply_id , body:Dict, user=Depends(require_role([UserRole.USER,UserRole.ADMIN]) )):
     user_id = user["user_id"]
     role = user["role"]
     return {
        "success":True,
        "message": "Request Successful - Updated Comment",
        "data": db.update_reply(int(comment_id), int(reply_id), body, user_id, role)}

