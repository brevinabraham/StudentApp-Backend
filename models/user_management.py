from pydantic import BaseModel


class RegBase(BaseModel):
    fname: str
    lname: str
    dob_dd: int
    dob_mm: int
    dob_yy: int
    email: str
    student: bool
    teacher: bool


class Credentials(BaseModel):
    user_id: str
    otherdetails: str
