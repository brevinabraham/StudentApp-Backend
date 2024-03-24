import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
from fastapi import FastAPI
from routes.routes import router
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

dotenv_path = os.getenv('MONGOURL')
load_dotenv(dotenv_path=dotenv_path)
client = MongoClient(os.getenv('MONGOURL'),
                     server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware,
                   secret_key=os.getenv('SESSIONMIDDLEWARE_KEY'))

app.include_router(router)
