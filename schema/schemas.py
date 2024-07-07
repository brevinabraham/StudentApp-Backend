from datetime import datetime, timedelta


def individual_question_user_creation(question) -> dict:
    return {
        "id": str(question["_id"]),
        "title": question["title"],
        "question": question["question"],
        "keyboardtype": question["keyboardtype"],
        "var_id": question["var_id"],
        "autocomplete": question["autocomplete"],
        "secure": question["secure"]
    }


def list_quesiton_user_creation(questions) -> list:
    return [individual_question_user_creation(question) for question in questions]

def individual_user(user) -> dict:
    return {
        "id": str(user["_id"]),
        "fname": user["fname"],
        "lname": user["lname"],
        "dob": user["dob"],
        "email": user["email"],
        "password": user["password"],
        "role": user["role"]
    }

def create_session(user_id: str, expires_delta: timedelta):
    now = datetime.now()
    session = {
        "user_id": user_id,
        "created_at": now,
        "expires_at": now + expires_delta
    }
    return session
