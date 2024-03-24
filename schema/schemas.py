def individual_question(question) -> dict:
    return {
        "id": str(question["_id"]),
        "title": question["title"],
        "question": question["question"],
        "keyboardtype": question["keyboardtype"],
        "var_id": question["var_id"],
        "autocomplete": question["autocomplete"],
        "secure": question["secure"]
    }


def list_quesiton(questions) -> list:
    return [individual_question(question) for question in questions]


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
