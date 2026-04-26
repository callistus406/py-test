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



1. add timestamp to all the records
2. complete the task enpoints
3. add comment feature
4. add authentication 
5. add a search filter to the get task endpoint

:wq