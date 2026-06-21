
from fastapi import FastAPI, Request, Query, status, HTTPException,Body,Depends
import json
from models import Create_User, Filter_Task,Update_task, Update_comment,Update_reply, Create_Task, Create_comment,Login_DTO,Login_Response,UserRole,Get_Task_Response,ApiResponse
import database
from typing  import Optional,Dict
from fastapi.responses import JSONResponse
import logging
from middleware import validate_token,validate_admin,require_role

app = FastAPI()

db = database.Database()


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


@app.exception_handler(HTTPException)
async def http_exception_handler(request:Request,exc:HTTPException):
    # logger.error("... Running exception interceptor")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail,
        }
    )

# ========================|| Authentication endpoints ||====================================

@app.post("/login", response_model=Login_Response,status_code=status.HTTP_200_OK )
def login(user: Login_DTO):
    return db.login(user)



@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: Create_User):
    return db.create_user(user)


# ========================|| User endpoints ||====================================

@app.get("/users", status_code=status.HTTP_200_OK)
def getUsers(user=Depends(require_role([UserRole.ADMIN]))):
    print(user)
    return {"data": db.get_users()}


@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int,user=Depends(require_role([UserRole.ADMIN]))):
    return {"data": db.get_user(user_id)}

# ========================|| Task endpoints ||====================================

@app.post("/tasks", status_code=status.HTTP_200_OK)
def create_task(task:Create_Task):
    return {"data": db.create_task(task)}

@app.delete("/tasks/{id}", status_code=status.HTTP_200_OK)
def delete_task(id:int,user=Depends(require_role([UserRole.USER,UserRole.ADMIN]))):
    user_id = user["user_id"]
    role = user["role"]
    return {"data": db.delete_task(user_id,id,role)}



# filter endpoint
@app.get("/tasks", status_code=status.HTTP_200_OK, response_model=ApiResponse[Get_Task_Response])
def filter_tasks(
    status: Optional [str] = None,
    priority: Optional [str] = None,
    page: Optional [int] = 1,
    limit: Optional [int] =20,
    search: Optional [str]= Query(None), 
   
):
    response =  db.filter_task_(status,priority,page,limit,search)
    return   {
        "success":True,
        "message": "Request Successful",
        "data": response
    }



@app.get("/tasks/{task_id}", status_code=status.HTTP_200_OK , response_model=ApiResponse[Get_Task_Response])
def get_task(task_id):
    response = db.get_task(int(task_id))
    print(response)
    return  {
        "success":True,
        "message": "Request Successful",
        "data": response
    }


@app.put("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def update_task(task_id,body:Update_task):
    return db.update_task_(int(task_id), body)

# ========================|| Comment endpoints ||====================================

@app.get("/comments", status_code=status.HTTP_200_OK)
def get_all_comment():
    return {"data": db.get_all_comment()}

@app.post("/create_commment", status_code = status.HTTP_200_OK)
def create_comment(data:Create_comment):
    return{"data": db.create_comment(data)}

@app.get("/comments/{comment_id}", status_code=status.HTTP_200_OK)
def get_comment(comment_id):
    return {"data": db.get_comment(int(comment_id))}

@app.delete("/comments/{comment_id}/x{task_id}", status_code=status.HTTP_200_OK)
def delete_comment(comment_id,user_id,task_id, user= Depends(validate_token)):
   user_id = user["user_id"]
   return {"data": db.delete_comment(int(comment_id),int(user_id),int(task_id))}

@app.put("/comments/{comment_id}/{reply_id}", status_code=status.HTTP_200_OK)
def update_reply(comment_id, reply_id , body:Dict ):
    return {"data": db.update_reply(int(comment_id), int(reply_id), body)}

