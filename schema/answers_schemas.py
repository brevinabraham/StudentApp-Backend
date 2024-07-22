

def individual_answer(answer) -> dict:
    return {
        "id": str(answer["_id"]),
        "question_id": str(answer["question_id"]),
        "user_id": answer["user_id"],
        "content": answer["content"],
        "created_at": answer["created_at"],
        "updated_at": answer["updated_at"],
        "like_count": answer["like_count"],
        "version": answer["version"],
    }


def list_answers(answers) -> list:
    return [individual_answer(answer) for answer in answers]
