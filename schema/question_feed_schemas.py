def individual_question_for_feed(question) -> dict:
    return {
        "id": str(question["_id"]),
        "title": question["title"],
        "inputType": question["inputType"],
        "required": question["required"]
    }


def list_individual_question_for_feed(questions) -> list:
    return [individual_question_for_feed(question) for question in questions]



def feed_individual_question(question) -> dict:
    return {
        "id": str(question["_id"]),
        "user_id": question["user_id"],
        "title": question["title"],
        "content": question["content"],
        "created_at": question["created_at"],
        "updated_at": question["updated_at"],
        "status_id": question["status_id"],
        "tags_id": question["tags_id"],
        "topic_id": question["topic_id"],
        "subtopic_id": question["subtopic_id"]
    }


def feed_list_quesiton(questions) -> list:
    return [feed_individual_question(question) for question in questions]

