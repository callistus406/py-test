from fastapi import FastAPI, Request, Query, status, HTTPException,Body
import json
from models import Create_User, Filter_Task,Update_task, Update_comment
import database
from typing  import Optional
from models import Update_task


app = FastAPI()

db = database.Database()


@app.post("/register", status_code=status.HTTP_201_CREATED)
def createItem(user: Create_User):
    return db.create_user(user)


@app.get("/users", status_code=status.HTTP_200_OK)
def createItem():
    return {"data": db.get_users()}


@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int):
    return {"data": db.get_user(user_id)}

# task endpoints

# filter endpoint
@app.get("/tasks", status_code=status.HTTP_200_OK)
def filter_tasks(
    status: Optional [str] = None,
    priority: Optional [str] = None,
    page: Optional [int] = 1,
    limit: Optional [int] = 50
):
    return {"data": db.filter_task_(status,priority,page,limit)}


@app.get("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def get_task(task_id):
    return {"data": db.get_task(int(task_id))}


@app.put("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def update_task(task_id,body:Update_task):
    return db.update_task_(int(task_id), body)
@app.get("/comments", status_code=status.HTTP_200_OK)
def get_all_comment():
    return {"data": db.get_all_comment()}

@app.get("/comments/{comment_id}", status_code=status.HTTP_200_OK)
def get_comment(comment_id):
    return {"data": db.get_comment(int(comment_id))}

@app.delete("/comments/{comment_id}/{user_id}/{task_id}", status_code=status.HTTP_200_OK)
def delete_comment(comment_id,user_id,task_id):
   return {"data": db.delete_comment(int(comment_id),int(user_id),int(task_id))}

@app.put("/comments/{comment_id}", status_code=status.HTTP_200_OK)
def update_comment(comment_id, body:Update_comment ):
    return {"data": db.update_comment(int(comment_id),body)}

