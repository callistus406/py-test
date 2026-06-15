from fastapi.security import OAuth2PasswordBearer

from jose import jwt
from database import SECRET,ALGO
from fastapi import HTTPException,status,Depends
from typing import List
from models import UserRole

extract_token = OAuth2PasswordBearer(tokenUrl="login")


def validate_token(token:str=Depends(extract_token)):
    try:
        payload = jwt.decode(token=token,key=SECRET,algorithms=[ALGO])
        user_id  = payload["sub"]
        role = payload["role"]
        if user_id is None:
            raise HTTPException(detail="Invalid token",status_code=401) 
        print({
            "user_id": user_id,
            "role": role
        })
        return{
            "user_id": user_id,
            "role": role
        }
    except Exception as e:
        print(e)
        raise HTTPException(detail="Invalid or expired token", status_code=401)



def require_role(roles:List[str]):
    def confirm_role(current_user = Depends(validate_token)):
        role = current_user["role"]

        if role  not in roles:
            raise HTTPException(detail="You are not allowed to access this resource",status_code=403)
        else:
            print(current_user,"tyuiuytrtyuiuytyuio")
            
            return current_user
    
    return confirm_role






def validate_user_or_admin():
    print(require_role([UserRole.USER,UserRole.ADMIN]))
    
    return require_role([UserRole.USER,UserRole.ADMIN])


def validate_admin():
    return require_role([UserRole.ADMIN])

def validate_user():
    return require_role([UserRole.USER])