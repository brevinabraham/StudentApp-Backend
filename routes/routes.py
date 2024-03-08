from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
from fastapi import APIRouter
from models.user_management import RegBase
from config.database import user_collection
from config.database import user_questions_collections
from schema.schemas import list_users
from schema.schemas import list_quesiton
from bson import ObjectId
from datetime import datetime


router = APIRouter()

@router.get("/")
async def get_user():
    users = list_users(user_collection.find())
    return users


@router.get("/questions/")
async def get_questions():
    print(datetime.now())
    questions = list_quesiton(user_questions_collections.find())
    return questions


@router.post("/")
async def post_user(reguser: RegBase):
    user_collection.insert_one(dict(reguser))


@router.put("/{id}")
async def put_user(id: str, user: RegBase):
    user_collection.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": dict(user)})


@router.delete("/{id}")
async def delete_user(id: str):
    user_collection.find_one_and_delete({"_id": ObjectId(id)})
