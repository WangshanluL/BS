from fastapi import APIRouter, Response, Depends, HTTPException, status
from captcha.image import ImageCaptcha
import random
from io import BytesIO
from pydantic import BaseModel
from typing import Optional
import datetime
import shutil
from fastapi.responses import JSONResponse
import os

router = APIRouter()
captcha = ImageCaptcha()


# 模拟数据库
class UserDB:
    def __init__(self):
        self.users = {
            "test@example.com": {
                "nick_name": "测试用户",
                "user_id": 10000000001,
                "is_admin": False,
                "email": "test@example.com",
                "password": "password123",
                "sex": "1",
                "person_description": "这是一个测试用户",
                "join_time": datetime.datetime.now() - datetime.timedelta(days=30),
                "last_login_time": datetime.datetime.now() - datetime.timedelta(days=2),
                "last_login_ip": "192.168.1.1",
                "last_login_ip_address": "北京市",
                "total_integral": 100,
                "current_integral": 80,
                "status": "1",
                "image": 10000000001
            }
        }
        self.messages = []

    def get_user_by_email(self, email):
        return self.users.get(email)

    def get_user_by_email_and_password(self, email, password):
        user = self.get_user_by_email(email)
        if user and user["password"] == password:
            return user
        return None

    def add_user(self, user_data):
        self.users[user_data["email"]] = user_data
        return user_data

    def add_message(self, message_data):
        self.messages.append(message_data)
        return message_data


# 实例化模拟数据库
user_db = UserDB()


# 请求模型
class LoginRequest(BaseModel):
    email: str
    password: str
    captcha: str


class RegisterRequest(BaseModel):
    email: str
    nickName: str
    password: str


# Generate a random captcha code
def generate_captcha():
    return ''.join(random.choices('0123456789', k=4))


# Store captcha code and its corresponding solution
captcha_store = {}


@router.get("/captcha")
async def get_captcha():
    captcha_code = generate_captcha()
    captcha_image = captcha.generate(captcha_code)
    captcha_store[captcha_code] = captcha_code.lower()

    # Convert image to bytes
    image_bytes = BytesIO()
    image_bytes.write(captcha_image.getvalue())
    image_bytes.seek(0)

    return Response(content=image_bytes.read(), media_type="image/png")


@router.post("/login")
async def login(request: LoginRequest):
    email = request.email
    password = request.password
    captcha_input = request.captcha

    # 验证码检查
    if captcha_input.lower() == captcha_store.get(captcha_input.lower()):
        user = user_db.get_user_by_email_and_password(email, password)

        if user:
            # 构建返回的用户数据
            data = {
                "nickName": user["nick_name"],
                "userId": user["user_id"],
                "isAdmin": user["is_admin"],
                "email": user["email"],
                "sex": user["sex"],
                "personDescription": user["person_description"],
                "joinTime": user["join_time"].strftime('%Y-%m-%d %H:%M:%S'),
                "lastLoginTime": user["last_login_time"].strftime('%Y-%m-%d %H:%M:%S'),
                "lastLoginIp": user["last_login_ip"],
                "lastLoginIpAddress": user["last_login_ip_address"],
                "totalIntegral": user["total_integral"],
                "currentIntegral": user["current_integral"],
                "status": user["status"]
            }
            return {"status": "success", "code": 200, "info": "登录成功", "data": data}
        else:
            return {"status": "error", "code": 402, "info": "邮箱或密码错误", "data": None}
    else:
        return {"status": "error", "code": 401, "info": "验证码错误，请重新输入", "data": None}


@router.post("/register")
async def register(request: RegisterRequest):
    email = request.email
    nick_name = request.nickName
    password = request.password
    user_id = random.randint(10000000000, 999999999999)

    # 检查邮箱是否已经注册过
    user = user_db.get_user_by_email(email)
    if user:
        return {"status": "error", "code": 404, "info": "该邮箱已被注册", "data": None}

    # 模拟复制 PNG 图片
    # 实际应用中应该确保 picture 目录存在并有正确的权限
    # 这里只是模拟这个过程
    # original_path = 'picture/original.jpg'
    # new_path = f'picture/{user_id}.jpg'
    # shutil.copyfile(original_path, new_path)

    # 创建新用户
    new_user = {
        "user_id": user_id,
        "email": email,
        "nick_name": nick_name,
        "password": password,
        "sex": "1",  # 默认男性
        "person_description": "",
        "join_time": datetime.datetime.now(),
        "last_login_time": datetime.datetime.now(),
        "last_login_ip": "",
        "last_login_ip_address": "",
        "total_integral": 0,
        "current_integral": 0,
        "status": "1",
        "is_admin": False,
        "image": user_id
    }

    # 添加用户到数据库
    user_db.add_user(new_user)

    # 向用户消息表添加一条消息
    message_content = "感谢注册，医智伴行欢迎您！以后的日子，小医陪您一起度过！"
    new_message = {
        "received_user_id": user_id,
        "article_id": None,
        "article_title": None,
        "comment_id": None,
        "send_user_id": None,
        "send_nick_name": None,
        "message_type": "0",  # 消息类型为注册欢迎消息
        "message_content": message_content,
        "status": "1",  # 消息状态为未读
        "create_time": datetime.datetime.now()
    }

    # 添加消息到数据库
    user_db.add_message(new_message)

    return {"status": "success", "code": 200, "info": "注册成功", "data": None}