
from fastapi import FastAPI, Request, Query, status, HTTPException,Body,Depends
import json
from schema.schema import Create_User, Filter_Task,Update_task, Update_comment,Update_reply,Update_User, Create_Task, Create_comment,Login_DTO,Login_Response,UserRole, ApiResponse,Get_Task_Response,UserResponse
import model.database as database
from typing  import Optional,Dict, TypeVar
from fastapi.responses import JSONResponse
import logging
from utils import logging
import time
from middleware.middleware import validate_token,validate_admin,require_role
from utils.token_blacklist import BlacklistToken
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    try:
        print(str(request.url).split("/")[-1])
        logging.logger.info(f"RequestID: {int(time.time())} - HOST:{request.client.host} - URL: {request.url}")

        response = await call_next(request)
        return response
    except Exception as e:
        logging.logger.error(e)


# @app.middleware("http")
# async def log_request(request:Request,call_next):
#     print("req")

db = database.Database()

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
# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["GET", "POST","PATCH"],
#     allow_headers=["*"],
# )

    
# ========================|| Authentication endpoints ||====================================

@app.post("/login", response_model=ApiResponse[Login_Response],status_code=status.HTTP_200_OK )
async def login(user: Login_DTO):
    
    return {"success": True,
    "message": "User retrieved successfully",
    "data": await db.login(user)}


@app.post("/register", status_code=status.HTTP_201_CREATED,response_model=ApiResponse[UserResponse]  )
async def register(user_data:Create_User):
    response  = await db.create_user(user_data)
    return {"success": True,
    "message": "User Created Successfully",
    "data": response}


# ========================|| User endpoints ||====================================

@app.get("/users", status_code=status.HTTP_200_OK,response_model=ApiResponse[UserResponse])
async def getUsers(user=Depends(require_role([UserRole.ADMIN]))):
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



@app.put("/users", status_code=status.HTTP_200_OK,response_model=ApiResponse)
async def update_user(body:Update_User, user=Depends(validate_token)):
    user_id = user["user_id"]
    response= await  db.update_user( body, user_id)
    return  {
        "success":True,
        "message": "Request Successful - fetched task by ID",
        "data": response
    }


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


@app.put("/tasks/{task_id}", status_code=status.HTTP_200_OK,response_model=ApiResponse[Get_Task_Response])
async def update_task(task_id: str,body:Update_task,user=Depends(require_role([UserRole.USER,UserRole.ADMIN]))):

    role = user["role"]  
    user_id = user["user_id"]
    response= await  db.update_task_(task_id, body, role, user_id)
    return  {
        "success":True,
        "message": "Request Successful - task updated",
        "data": response
    }

# ========================|| Comment endpoints ||====================================

@app.get("/comments", status_code=status.HTTP_200_OK,response_model=ApiResponse)
async def get_all_comment():
    return {
        "success":True,
        "message": "Request Successful Retrieved All Comments",
        "data": await db.get_all_comment()}

@app.post("/comments/{task_id}", status_code = status.HTTP_200_OK,response_model=ApiResponse)
async def create_comment(data:Create_comment,task_id: str,user= Depends(validate_token)):
    user_id = user["user_id"]
    return{
        "success":True,
        "message": "Request Successful Created a Comment",
        "data": await db.create_comment(data, user_id, task_id)}

@app.get("/comments/{comment_id}", status_code=status.HTTP_200_OK,response_model=ApiResponse)
async def get_comment(comment_id:str):
    return {
        "success":True,
        "message": "Request Successful Fetched Comment by ID",
        "data":await  db.get_comment(comment_id)}

@app.delete("/comments/{comment_id}/x{task_id}", status_code=status.HTTP_200_OK,response_model=ApiResponse)
def delete_comment(comment_id: str,  user=Depends(require_role([UserRole.USER,UserRole.ADMIN]))):
   user_id = user["user_id"]
   role = user["role"]
   return {
        "success":True,
        "message": "Request Successful Deleted Comment by ID",
       "data": db.delete_comment(comment_id,user_id,role)}

@app.put("/comments/{comment_id}/x{task_id}", status_code=status.HTTP_200_OK,response_model=ApiResponse)
def update_reply(comment_id:str , body:Dict,  user=Depends(validate_token) ):
     user_id = user["user_id"]
     return {
        "success":True,
        "message": "Request Successful - Updated Comment",
        "data": db.update_reply(comment_id, body, user_id, )}


@app.get("/health", status_code=status.HTTP_200_OK,response_model=ApiResponse)
def update_reply(  ):

     return {
        "success":True,
        "message": "Server is Up",
        "data": None
        }



# @app.post("/logout", status_code=status.HTTP_200_OK,response_model=ApiResponse)
# def update_reply(  user=Depends(validate_token) ):

#      blacklist = BlacklistToken()
#      blacklist.add_token(user["token"])
#      print(user["token"], "opioioi")
#      return {
#         "success":True,
#         "message": "Logout successful",
#         "data": None}



