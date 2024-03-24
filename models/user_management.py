from pydantic import BaseModel


class RegBase(BaseModel):
    fname: str
    lname: str
    dob: str
    email: str
    password: str
    roles: list


class User(BaseModel):
    email: str
    password: str
