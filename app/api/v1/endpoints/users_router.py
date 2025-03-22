from fastapi import APIRouter, Response, Depends, HTTPException, status, Request
from captcha.image import ImageCaptcha
import random
from io import BytesIO
from pydantic import BaseModel
from typing import Optional
import datetime
from fastapi.responses import JSONResponse
from app.schemas.loginAndRegisterSchema import LoginRequest, RegisterRequest
from app.services.user_service import user_service
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.database_dependency import get_db
from app.schemas.userSchema import UserCreate

router = APIRouter()
captcha = ImageCaptcha()


# Generate a random captcha code
def generate_captcha():
    return ''.join(random.choices('0123456789', k=4))


# Store captcha code and its corresponding solution
captcha_store = {}


@router.get("/captcha")
async def get_captcha():
    print("qaq")
    captcha_code = generate_captcha()
    captcha_image = captcha.generate(captcha_code)
    captcha_store[captcha_code] = captcha_code.lower()

    # Convert image to bytes
    image_bytes = BytesIO()
    image_bytes.write(captcha_image.getvalue())
    image_bytes.seek(0)

    return Response(content=image_bytes.read(), media_type="image/png")


@router.post("/login")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db), client_req: Request = None):
    email = request.email
    password = request.password
    captcha_input = request.captcha

    # 验证码检查
    if captcha_input.lower() == captcha_store.get(captcha_input.lower()):
        # 使用user_service替代原来的user_db
        user = await user_service.authenticate(db, email=email, password=password)

        if user:
            # 获取IP地址
            client_ip = client_req.client.host if client_req else ""
            ip_address = ""  # 实际应用中，应该获取IP地址的地理位置

            # 更新用户登录信息
            await user_service.update_login_info(db, user_id=user.user_id, ip=client_ip, ip_address=ip_address)

            # 构建返回的用户数据
            data = {
                "nickName": user.nick_name,
                "userId": user.user_id,
                "isAdmin": bool(user.is_admin),
                "email": user.email,
                "sex": user.sex,
                "personDescription": user.person_description,
                "joinTime": user.join_time.strftime('%Y-%m-%d %H:%M:%S'),
                "lastLoginTime": user.last_login_time.strftime('%Y-%m-%d %H:%M:%S'),
                "lastLoginIp": user.last_login_ip,
                "lastLoginIpAddress": user.last_login_ip_address,
                "totalIntegral": user.total_integral,
                "currentIntegral": user.current_integral,
                "status": user.status
            }
            return {"status": "success", "code": 200, "info": "登录成功", "data": data}
        else:
            return {"status": "error", "code": 402, "info": "邮箱或密码错误", "data": None}
    else:
        return {"status": "error", "code": 401, "info": "验证码错误，请重新输入", "data": None}


@router.post("/register")
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    email = request.email
    nick_name = request.nickName
    password = request.password

    # 检查邮箱是否已经注册过
    existing_user = await user_service.get_by_email(db, email=email)
    if existing_user:
        return {"status": "error", "code": 404, "info": "该邮箱已被注册", "data": None}

    # 创建新用户
    user_create = UserCreate(
        email=email,
        nick_name=nick_name,
        password=password,
        sex="1",  # 默认男性
        person_description="",
        total_integral=0,
        current_integral=0,
        last_login_ip="",
        last_login_ip_address=""
    )

    # 使用user_service创建用户
    user = await user_service.create_user(db, user_create=user_create)

    # 可以添加欢迎消息
    # await user_service.add_welcome_message(db, user.user_id)

    return {"status": "success", "code": 200, "info": "注册成功", "data": None}