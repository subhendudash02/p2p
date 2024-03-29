"""
This file contains schemas for signup and login and its response models.
"""

from pydantic import BaseModel

# For data creation


class UserData(BaseModel):
    username: str
    email: str
    

class SignUpData(UserData):
    password: str


class LoginData(BaseModel):
    username: str
    password: str


# For data response


class SignUpResponse(BaseModel):
    username: str
    email: str
    msg: str


class LoginResponse(BaseModel):
    username: str
    access_token: str
    msg: str

class ErrorResponse(BaseModel):
    detail: str