from fastapi import APIRouter, HTTPException, Request, Depends, Response
from models.question_feed import Question
from config.database import question_feed_user_questions
from schema.question_feed_schemas import feed_individual_question, feed_list_quesiton

feedsrouter = APIRouter()


@feedsrouter.post("/api/feeds/add_your_question")
async def create_question(question: Question):
    question_feed_user_questions.insert_one(dict(question))
    return {"message": "Question created successfully!"}


@feedsrouter.get("/api/feeds/questions")
async def get_questions():
    questions = feed_list_quesiton(question_feed_user_questions.find())
    return questions


@feedsrouter.delete("/api/feeds/delete_all_questions")
async def deleted():
    question_feed_user_questions.delete_many({})
