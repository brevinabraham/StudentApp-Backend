from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
from fastapi import APIRouter, HTTPException, Request, Depends, Response
from fastapi.responses import JSONResponse
from models.user_management import RegBase
from models.user_management import User
from config.database import user_collection, user_questions_collections, session_collection
from schema.schemas import list_quesiton, create_session, individual_session
from bson import ObjectId
from datetime import datetime, timedelta
from passlib.context import CryptContext
import bcrypt
import jwt
import os

router = APIRouter()

SECRET_KEY = os.getenv('SECRET_KEY').encode()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Not authenticated")
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Not authenticated")


def get_current_user_id(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = token.replace("Bearer ", "")
    user_id = decode_access_token(token)
    return user_id


@router.get("/api/user/{email}")
async def get_user(email: str):
    user = user_collection.find_one({"email": email})
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
    questions = list_quesiton(user_questions_collections.find())
    return questions


@router.post("/api/user")
async def post_user(reguser: RegBase):
    reguser.password = bcrypt.hashpw(
        reguser.password.encode('utf-8'), bcrypt.gensalt())
    user_collection.insert_one(dict(reguser))
    return {'message': 'complete'}


@router.post("/api/user/login")
async def login(user_data: User):
    user = user_collection.find_one({"email": user_data.email})
    if user is None:
        raise HTTPException(
            status_code=401, detail="Invalid email or password")

    hashed_password = user.get("password")
    if not bcrypt.checkpw(user_data.password.encode('utf-8'), hashed_password):
        raise HTTPException(
            status_code=401, detail="Invalid email or password")

    user_id = str(user["_id"])
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_id}, expires_delta=access_token_expires
    )
    # Create session
    session = create_session(user_id, access_token_expires)
    session_id = session_collection.insert_one(session).inserted_id

    # Convert datetime to string for JSON serialization
    session_data = {
        'session_id': str(session_id),
        'user_id': session['user_id'],
        'created_at': session['created_at'].isoformat(),
        'expires_at': session['expires_at'].isoformat()
    }

    return JSONResponse(content={
        'message': 'Login successful!',
        'access_token': access_token,
        'token_type': 'bearer',
        'session_id': session_data
    })


@router.get("/protected")
async def protected_route(user_id: str = Depends(get_current_user_id)):
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    for key, value in user.items():
        if key == '_id':
            user[key] = str(value)
        else:
            user[key] = value
    return {'data': user}


@router.post("/api/user/logout")
async def logout(response: Response, request: Request):
    session_id = request.headers.get("Session-ID")
    if session_id:
        session_collection.delete_one({"_id": ObjectId(session_id)})
    return {"message": "Logout successful!"}


@router.put("/api/user/{id}")
async def put_user(id: str, user: RegBase):
    user_collection.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": dict(user)})


@router.delete("/api/user/{id}")
async def delete_user(id: str):
    user_collection.find_one_and_delete({"_id": ObjectId(id)})
