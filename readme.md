<!-- user crud operations (mgt tasks)
admin (mgt endpoints)
comments
logs,
errorhandling, input validation, -->

<!-- 
users model:

username: str
email: str
name: str
is_active: boolean
role: 

Tasks model:
title: str
description: str
status: str \ pending| active| completed| 
priority: string| high| low | medium
start_date: str
end_date:str
user_id: int
created_by: int
updated_by: int
completed_at: Date



Comments:
task_id: int
user_id: int
comment: str
create_at: str

 -->

 <!-- create a task management api with these features -->
 <!-- user management  module-->
 <!-- task management module -->
 <!-- comment feature -->
 <!-- dashboard -->

comment= {
   "task_id: 1,
   "id" : 1,
   "userId": 2,
   "content": "this is from the admin",
   "replies": [
      {
      "id" : 1,
      "user": 2,
      "content": "this is a reply from the user",
      }
   ]
}



## search field should match text in title and description
## pagination should filter from 1 not 0
## create a metadate for show the pagination values and remaning dataset count
## add comment reply
## login and signup endpoint, role/access management(permission, amin etc, admin assigning task), 



# Add Logging
# implement authentication with jwt
# Exception handling
# middleware implementation


# validate the password, 1 uppercase numbers, , length should be ? 8 + special character
# fix the error handling
#  hashlib => bcrypt

# add validate token for endpoints, add response body for other endpoints - task, comments, response

#threading
<!-- types of databases : 
-relational database - makes use of rows and columns, oyu have a database that relates to another table, e.g mysql, microsodt derver, postquest. Main purpose is to main integrity

-nonrelational database - doesn't rely and column and rows, data is stored in document format, and can be stored in json format, e.g mongodb

Relational databases organize data into strict, tabular rows and columns with predefined schemas, using SQL to link multiple tables. Non-relational databases (NoSQL) offer flexible, schema-less structures like key-value pairs or documents to handle unstructured data and scale horizontally across servers -->


<!-- MONGO_URL = "mongodb+srv://neme_python:test123@info-3139.fvv8kuz.mongodb.net/?appName=INFO-3139/task_manger"
DATABASE = "task_manger" -->




        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2YTUxMmM0NDU5ZGYzZjY0NjIzNWJkMzUiLCJyb2xlIjoiQWRtaW4ifQ.cqVOrjOu1XHQGgkvMX8olF2XS6YlMNoez667xp3Me_o"

Things to put in to consideration when building an Authentication System
-access token
-refresh token

topic of the day-how to blacklist token - 28/07/26 
any yoken voided will not be passed through the authentication middleware - this will be performed using redis - this is a temp database to store data wehardly access


eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2YTUxMmM0NDU5ZGYzZjY0NjIzNWJkMzUiLCJyb2xlIjoidXNlciJ9.-T3zy7yS-ulhLELvIqXO-jd3AfKGcjuMYcHZzWjc7XI

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2YTUxMmM0NDU5ZGYzZjY0NjIzNWJkMzUiLCJyb2xlIjoidXNlciJ9.-T3zy7yS-ulhLELvIqXO-jd3AfKGcjuMYcHZzWjc7XI

note
docker : you can package, deploy your application, so you can run on any platform without any compatability issue

Virtual Machine - running a full guest Operating systen on a hypervisor hardware

you can create different docker image to apply different versions, and port number but will have the same codebase and framework

-Volumes - essential for persistent storage on our host operating system, temp storage incase of deltetion or crashes

TO CREATE AN IMAGE
1. create a file called DockerFile vscode

docker run -d 
- foreground vs background?

steps 
build the docker  - create an image
run docker -d create a unit that runs the image
docker run -p 8000:8000 --name fastapi-app dastapi-server




next class we are looking at networking in docker
