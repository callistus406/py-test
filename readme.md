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