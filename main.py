from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
from fastapi import FastAPI
from routes.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['exp://192.168.1.213:8081', 'http://localhost:19006'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
