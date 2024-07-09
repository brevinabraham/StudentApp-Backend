from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import os

dotenv_path = os.getenv('MONGOURL')
load_dotenv(dotenv_path=dotenv_path)
client = MongoClient(os.getenv('MONGOURL'))

db_user_management = client['user_management_db']
db_question_feed = client['question_feed_db']


user_collection = db_user_management["user_collection"]
user_questions_collections = db_user_management["questions"]
user_session_collection = db_user_management["session_collection"]

question_feed_user_questions = db_question_feed['user_questions']
question_feed_user_question_templates = db_question_feed['question_template']
