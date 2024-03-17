from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
from fastapi import APIRouter
from fastapi import HTTPException
from models.user_management import RegBase
from config.database import user_collection
from config.database import user_questions_collections
from schema.schemas import list_users
from schema.schemas import list_quesiton
from bson import ObjectId
from datetime import datetime


router = APIRouter()


@router.get("/{email}")
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


@router.post("/")
async def post_user(reguser: RegBase):
    user_collection.insert_one(dict(reguser))
    return {'message': 'complete'}


@router.put("/{id}")
async def put_user(id: str, user: RegBase):
    user_collection.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": dict(user)})


@router.delete("/{id}")
async def delete_user(id: str):
    user_collection.find_one_and_delete({"_id": ObjectId(id)})
