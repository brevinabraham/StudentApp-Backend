from fastapi import APIRouter, HTTPException, Request, Depends, Response
from models.question_feed import Question, UpdateQuestion
from config.database import question_feed_user_questions, question_feed_user_question_templates, question_statuses, db_answers, db_question_likes
from schema.question_feed_schemas import feed_list_quesiton, list_individual_question_for_feed, list_question_statuses
from bson import ObjectId

feedsrouter = APIRouter()


@feedsrouter.post("/api/feeds/add_your_question")
async def create_question(question: Question):
    question_feed_user_questions.insert_one(dict(question))
    return {"message": "Question created successfully!"}


@feedsrouter.get("/api/feeds/questions")
async def get_questions():
    questions = feed_list_quesiton(question_feed_user_questions.find())
    return questions


@feedsrouter.get("/api/feeds/getQuestion")
async def get_question(id: str):
    question = question_feed_user_questions.find_one({"_id": ObjectId(id)})
    question["_id"] = str(question["_id"])
    return question


@feedsrouter.delete("/api/feeds/delete_all_questions")
async def deleted():
    question_feed_user_questions.delete_many({})


@feedsrouter.get("/api/feeds/questions_template/")
async def get_questions():
    questions = list_individual_question_for_feed(
        question_feed_user_question_templates.find())
    return questions


@feedsrouter.delete("/api/feeds/questions/rm/")  # remove q
async def delete_user(id: str):
    question_feed_user_questions.find_one_and_delete({"_id": ObjectId(id)})
    db_answers.delete_many({"question_id": id})
    return {'message': 'sucessfully deleted'}


@feedsrouter.put("/api/feeds/questions/edit/")
async def put_question(id: str, question: UpdateQuestion):
    result = question_feed_user_questions.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": dict(question)})

    if result is None:
        raise HTTPException(status_code=404, detail="Question not found")

    return {'message': 'successfully updated'}


@feedsrouter.put("/api/feeds/question/like")
async def addLike(userid: str, questionid: str):
    existLike = db_question_likes.count_documents(
        {"$and": [{"user_id": userid}, {"question_id": questionid}]})
    print(existLike)
    if existLike > 0:
        return {"message": "alreadyliked"}
    db_question_likes.insert_one(
        {"user_id": userid, "question_id": questionid})
    question_feed_user_questions.find_one_and_update(
        {"_id": ObjectId(questionid)}, {"$inc": {"like_count": 1}})
