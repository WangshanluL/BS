from typing import Optional, List, Dict, Any, Union
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import user_repository
from app.schemas.userSchema import UserCreate, UserUpdate, UserInDB

import uuid
from datetime import datetime


class UserService:
    async def get_by_id(self, db: AsyncSession, user_id: str) -> Optional[UserInDB]:
        """Get user by user_id"""
        user = await user_repository.get_by_user_id(db, user_id=user_id)
        if user:
            return UserInDB.from_orm(user)
        return None

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[UserInDB]:
        """Get user by email"""
        user = await user_repository.get_by_email(db, email=email)
        if user:
            return UserInDB.from_orm(user)
        return None

    async def create_user(self, db: AsyncSession, user_create: UserCreate) -> UserInDB:
        """Create a new user"""
        # Generate a unique user ID
        user_id = str(uuid.uuid4().int)[:15]

        user_data = user_create.dict()
        user_data.update({
            "user_id": user_id,
            "password": user_create.password,
            "join_time": datetime.now(),
            "last_login_time": datetime.now(),
            "status": 1,
            "is_admin": 0
        })

        db_user = await user_repository.create(db, obj_in=user_data)
        return UserInDB.from_orm(db_user)

    async def authenticate(self, db: AsyncSession, email: str, password: str) -> Optional[UserInDB]:
        """Authenticate user with email and password"""
        user = await user_repository.get_by_email(db, email=email)
        if not user:
            return None
        if not password == user.password:
            return None
        return UserInDB.from_orm(user)

    async def update_login_info(self, db: AsyncSession, user_id: str, ip: str, ip_address: str) -> Optional[UserInDB]:
        """Update user's last login information"""
        user = await user_repository.get_by_user_id(db, user_id=user_id)
        if not user:
            return None

        updated_user = await user_repository.update_last_login(db, user=user, ip=ip, ip_address=ip_address)
        return UserInDB.from_orm(updated_user)

    async def add_user_integral(self, db: AsyncSession, user_id: str, oper_type: int, integral: int) -> bool:
        """Add user integral"""
        record = await user_repository.add_integral(db, user_id=user_id, oper_type=oper_type, integral=integral)
        return record is not None

    async def save_email_verification_code(self, db: AsyncSession, email: str, code: str) -> bool:
        """Save email verification code"""
        code_obj = await user_repository.save_email_code(db, email=email, code=code)
        return code_obj is not None

    async def verify_email_code(self, db: AsyncSession, email: str, code: str) -> bool:
        """Verify email verification code"""
        return await user_repository.verify_email_code(db, email=email, code=code)

    async def add_welcome_message(self, db: AsyncSession, user_id: str, message_content: str = None) -> bool:
        """Add welcome message for new user

        Note: This is a placeholder. You need to implement the actual message repository
        and service to make this work.
        """
        # This is a placeholder for the actual implementation
        # You would need to create a message_repository and possibly a message_service
        if message_content is None:
            message_content = "感谢注册，医智伴行欢迎您！以后的日子，小医陪您一起度过！"

        # TODO: Implement message creation logic
        # Example implementation:
        # new_message = {
        #     "received_user_id": user_id,
        #     "message_type": "0",  # Message type for welcome message
        #     "message_content": message_content,
        #     "status": "1",  # Unread status
        #     "create_time": datetime.now()
        # }
        # result = await message_repository.create(db, new_message)
        # return result is not None

        # For now, return True to indicate success
        return True


user_service = UserService()