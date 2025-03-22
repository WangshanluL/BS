from typing import Optional
from pydantic import BaseModel, EmailStr, validator, Field
from datetime import datetime
class LoginRequest(BaseModel):
    email: str
    password: str
    captcha: str


class RegisterRequest(BaseModel):
    email: str
    nickName: str
    password: str
