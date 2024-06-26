from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
from fastapi import APIRouter, HTTPException, Request, Depends, Response
from fastapi.responses import JSONResponse
from models.user_management import RegBase
from models.user_management import User
from config.database import user_collection
from config.database import user_questions_collections
from schema.schemas import list_quesiton
from bson import ObjectId
from datetime import datetime
from passlib.context import CryptContext
import bcrypt
from cryptography.fernet import Fernet
import base64
import os

router = APIRouter()

SECRET_KEY = os.getenv('SECRET_KEY').encode()
cipher_suite = Fernet(SECRET_KEY)


def encrypt_user_id(user_id: str) -> str:
    encrypted_text = cipher_suite.encrypt(user_id.encode())
    return base64.urlsafe_b64encode(encrypted_text).decode()


def decrypt_user_id(encrypted_user_id: str) -> str:
    decoded_encrypted_text = base64.urlsafe_b64decode(
        encrypted_user_id.encode())
    decrypted_text = cipher_suite.decrypt(decoded_encrypted_text)
    return decrypted_text.decode()


def get_current_user_id(request: Request):
    encrypted_user_id = request.cookies.get("userId")
    if not encrypted_user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user_id = decrypt_user_id(encrypted_user_id)
    return user_id


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

    user_id = str(user["_id"])
    encrypted_user_id = encrypt_user_id(user_id)

    response = JSONResponse(
        content={'message': 'Login successful!', 'userId': encrypted_user_id})
    response.set_cookie(key="userId", value=encrypted_user_id,
                        httponly=True, secure=True, samesite='None')
    return response

@router.get("/protected")
async def protected_route(user_id: str = Depends(get_current_user_id)):

    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    for key, value in user.items():
        if key == '_id':
            user[key] = str(value)
        else:
            user[key] = value
    return {'data': user}


@router.post("/api/user/logout")
async def logout(response: Response):
    response.delete_cookie("userId")
    return {"message": "Logout successful!"}


@router.put("/api/user/{id}")
async def put_user(id: str, user: RegBase):
    user_collection.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": dict(user)})


@router.delete("/api/user/{id}")
async def delete_user(id: str):
    user_collection.find_one_and_delete({"_id": ObjectId(id)})
