from typing import Optional
from pydantic import BaseModel, EmailStr, validator, Field, ConfigDict
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    nick_name: Optional[str] = None  # 改为可选
    sex: Optional[int] = None
    person_description: Optional[str] = None
    image: Optional[str] = None


class UserCreate(UserBase):
    password: str

    @validator('password')
    def password_must_be_strong(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


class UserUpdate(BaseModel):
    nick_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    sex: Optional[int] = None
    person_description: Optional[str] = None
    image: Optional[str] = None
    status: Optional[int] = None


class UserInDBBase(UserBase):
    user_id: str
    join_time: datetime
    last_login_time: Optional[datetime] = None
    last_login_ip: Optional[str] = None  # 添加这个字段
    last_login_ip_address: Optional[str] = None  # 可能也需要添加这个字段
    total_integral: int
    current_integral: int
    status: int
    is_admin: int

    model_config = ConfigDict(from_attributes=True)  # 新版Pydantic配置


class UserInDB(UserInDBBase):
    password: str


class User(UserInDBBase):
    pass


class UserWithToken(User):
    access_token: str
    token_type: str = "bearer"