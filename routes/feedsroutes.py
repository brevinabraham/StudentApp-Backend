from fastapi import APIRouter, HTTPException, Request, Depends, Response
from models.question_feed import Question
from config.database import question_feed_user_questions, question_feed_user_question_templates, question_statuses
from schema.question_feed_schemas import feed_list_quesiton, list_individual_question_for_feed, list_question_statuses

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


@feedsrouter.get("/api/feeds/questions_template/")
async def get_questions():
    questions = list_individual_question_for_feed(
        question_feed_user_question_templates.find())
    return questions
