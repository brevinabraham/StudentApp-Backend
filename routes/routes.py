from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
from fastapi import APIRouter, HTTPException, Request, Depends

from models.user_management import RegBase
from models.user_management import User
from config.database import user_collection
from config.database import user_questions_collections
from schema.schemas import list_quesiton
from bson import ObjectId
from datetime import datetime
from passlib.context import CryptContext
import bcrypt


router = APIRouter()


@router.get("/api/user/{email}")
async def get_user(email: str):
    user = user_collection.find_one(
        {"email": email}
    )
    if user is None:
        return {'message': "user doesn't exist", "bool": False}
    else:
        for key, value in user.items():
            if key == '_id':
                user[key] = str(value)
            else:
                user[key] = value
        return {'message': 'user found', 'userRole': user["role"], "bool": True, "userID": user["_id"]}



@router.get("/questions/")
async def get_questions():
    print(datetime.now())
    questions = list_quesiton(user_questions_collections.find())
    return questions


@router.post("/api/user")
async def post_user(reguser: RegBase):
    reguser.password = bcrypt.hashpw(
        reguser.password.encode('utf-8'), bcrypt.gensalt())
    user_collection.insert_one(dict(reguser))
    return {'message': 'complete'}


@router.post("/api/user/login")
async def login(request: Request, user_data: User):
    user = user_collection.find_one({"email": user_data.email})
    if user is None:
        raise HTTPException(
            status_code=401, detail="Invalid email or password")

    hashed_password = user.get("password")
    if not bcrypt.checkpw(user_data.password.encode('utf-8'), hashed_password):
        raise HTTPException(
            status_code=401, detail="Invalid email or password")

    request.session["user_id"] = str(user["_id"])
    return {'message': 'Login successful!', 'userId': str(user["_id"])}


def get_current_user_id(request: Request):
    return request.session.get("user_id")


@router.get("/protected")
async def protected_route(user_id: str = Depends(get_current_user_id)):
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {'data': user_collection.find_one({"_id": ObjectId(user_id)})}


@router.post("/api/user/logout")
async def logout(request: Request):
    request.session.clear()
    return {"message": "Logout successful!"}


@router.put("/api/user/{id}")
async def put_user(id: str, user: RegBase):
    user_collection.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": dict(user)})


@router.delete("/api/user/{id}")
async def delete_user(id: str):
    user_collection.find_one_and_delete({"_id": ObjectId(id)})
