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

[ 
{
    "property": "value"
 },
 {
    "property": "value"
 }
 ]


 Dict[str, Any]



 #     def update_user(self, id:int, username:str, name:str, email:str, isactive: bool, role:str):
#         for data in self.user:
#             if(self.user["id"] == id):
#                 self.user["id"] = id
#                 self.user["username"] = username
#                 self.user["name"] = name
#                 self.user["email"] = email
#                 self.user["isactive"] = isactive
#                 self.user["role"] = role
                
        

#     def add_user(self, id:int, username:str, name:str, email:str, isactive: bool, role:str):
#             for data in self.user:
#                 if(self.user["id"] == id):
#                     self.user["id"] = id
#                     self.user["username"] = username
#                     self.user["name"] = name
#                     self.user["email"] = email
#                     self.user["isactive"] = isactive
#                     self.user["role"] = role
                

#     def getAll_user(self,):
#         for data in self.user:
#             return self.user

#     def delete_user(self,id:int):
#         for data in self.user: 
#             del self.user[id] 

# #task queries

#     def create_task(self, tasks:models.Create_task):
#        self.tasks.append
#        ({ 
#             tasks
#         })

#     def update_task(self, title: str, description:str,  status:str,priority:str, start_date: str, end_date:str):
#          for data in self.tasks:
#                 if(self.tasks["id"] == id):
#                     self.tasks["id"] = id
#                     self.tasks["title"] = title
#                     self.tasks["description"] = description
#                     self.tasks["status"] = status
#                     self.tasks["priority"] = priority
#                     self.tasks["start_date"] = start_date
#                     self.tasks["end_date"] = end_date
    
#     def add_task(self, title: str, description:str,  status:str,priority:str, start_date: str, end_date:str):
#               for data in self.tasks:
#                 if(self.tasks["id"] == id):
#                     self.tasks["id"] = id
#                     self.tasks["title"] = title
#                     self.tasks["description"] = description
#                     self.tasks["status"] = status
#                     self.tasks["priority"] = priority
#                     self.tasks["start_date"] = start_date
#                     self.tasks["end_date"] = end_date
    
    
#     def getAll_task(self,):
#         for data in self.tasks:
#             return self.task
    
#     def getTask(self, id:int):
#         for data in self.tasks:
#             return self.tasks[id]
        
#     def deleteTask(self,id:int):
#         for data in self.tasks: 
#             del self.tasks[id] 
    
#     def viewTask(self,):
#         return self.tasks

# #comments queries
# def createComment(self, comments:models.Create_comment):
#     self.comments.append(
#         {
#             comments
#         }
#     )

# def getComment(self, id:int):
#     for data in self.comments:
#             return self.comments[id]
        
# def deleteComment(self,id:int):
#         for data in self.comments: 
#             del self.comments[id] 
    
# def viewComment(self,):
#         return self.comments

# def addComments(self, task_id: int,user_id: int,comment: str,create_at: str):
#      for data in self.comments:
#           if(self.comments["task_id"] == task_id):
#                self.comments["user_id"] = user_id
#                self.comments["comment"] = comment
#                self.comments["create_at"] = create_at