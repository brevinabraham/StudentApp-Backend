def feed_individual_question(question) -> dict:
    return {
        "id": str(question["_id"]),
        "user_id": question["user_id"],
        "title": question["title"],
        "content": question["content"],
        "created_at": question["created_at"],
        "updated_at": question["updated_at"],
        "status": question["status"],
        "tags": question["tags"]
    }


def feed_list_quesiton(questions) -> list:
    return [feed_individual_question(question) for question in questions]
