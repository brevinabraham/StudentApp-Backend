from pydantic import BaseModel

class RegBase(BaseModel):
    fname: str
    lname: str
    dob: str
    email: str
    role: list
