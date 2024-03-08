from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import os

dotenv_path = os.getenv('MONGOURL')
load_dotenv(dotenv_path=dotenv_path)
client = MongoClient(os.getenv('MONGOURL'))

db = client['user_management_db']


user_collection = db["user_collection"]
user_questions_collections = db["questions"]
