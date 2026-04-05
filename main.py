from fastapi import FastAPI, Request, Query, status, HTTPException
import json
from models import Create_User
import database


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

@app.get("/tasks", status_code=status.HTTP_200_OK)
def get_tasks():
    return {"data": db.get_tasks()}
@app.get("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def get_task(task_id):
    return {"data": db.get_task(int(task_id))}