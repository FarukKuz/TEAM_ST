from pydantic import BaseModel

class UserIn(BaseModel):
    uid: str
    email: str
    username: str
    profile_picture: str = ""
    login_type: str

class UserUID(BaseModel):
    uid: str
