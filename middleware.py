from fastapi.security import OAuth2PasswordBearer

from jose import jwt
from database import SECRET,ALGO
from fastapi import HTTPException,status,Depends

extract_token = OAuth2PasswordBearer(tokenUrl="login")


def validate_token(token:str=Depends(extract_token)):
    try:

        payload = jwt.decode(token=token,key=SECRET,algorithms=[ALGO])
        print(payload)

        user_id  = payload["sub"]

        if user_id is None:
            raise HTTPException(detail="Invalid token",status_code=401)
        
        return{
            "user_id": user_id
        }
    except Exception as e:
        print(e)
        raise HTTPException(detail="Invalid or expired token", status_code=401)
