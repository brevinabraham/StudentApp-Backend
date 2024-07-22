from fastapi import APIRouter, HTTPException, Request, Depends, Response
from models.answers import Answers
from config.database import db_answers
from schema.answers_schemas import individual_answer, list_answers
from bson import ObjectId

answerrouter = APIRouter()


@answerrouter.post("/api/question/answer")
async def create_answer(answer: Answers):
    db_answers.insert_one(dict(answer))
    return {"message": "Answer created"}


# @feedsrouter.get("/api/feeds/questions")
# async def get_questions():
#     questions = feed_list_quesiton(question_feed_user_questions.find())
#     return questions


@answerrouter.get("/api/question/answers")
async def get_answers(id: str):
    answers = list_answers(db_answers.find({"question_id": id}))
    return answers
