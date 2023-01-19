from fastapi import FastAPI , HTTPException , status
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.User.schema import User
from app.User.model import UserData
from database.db import SessionLocal
from uuid import uuid4
from datetime import datetime

router = APIRouter()
db = SessionLocal()

@router.get('/get_user,{user_id}')
def get_user(user_id : int):
    user = db.query(UserData).filter(UserData.user_id == user_id).first()

    if user is None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST , detail = "user not found")

    return{'data' : user , "message" : "user retrived successfully"}


@router.post('/user')
def create_user(user : User):
    db_user = db.query(UserData).filter(UserData.user_name == user.user_name).first()

    if db_user is not None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST , detail = "User already exist")

    new_user = UserData(
        user_name = user.user_name,
        user_id = uuid4(),
        created_at = datetime.utcnow(),
        is_deleted = user.is_deleted

    )

    db.add(new_user)
    db.commit()
    return {"status" : status.HTTP_201_CREATED , "message" : "user created successfully"}



    

    







