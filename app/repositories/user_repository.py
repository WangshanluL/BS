from typing import Dict, Any, Optional, List, Union
from sqlalchemy.orm import Session
from app.db.models.user import UserInfo, EmailCode, UserIntegralRecord
from datetime import datetime


class UserRepository:
    def get_by_user_id(self, db: Session, user_id: str) -> Optional[UserInfo]:
        """Get user by user_id"""
        return db.query(UserInfo).filter(UserInfo.user_id == user_id).first()

    def get_by_email(self, db: Session, email: str) -> Optional[UserInfo]:
        """Get user by email"""
        return db.query(UserInfo).filter(UserInfo.email == email).first()

    def get_by_nick_name(self, db: Session, nick_name: str) -> Optional[UserInfo]:
        """Get user by nick_name"""
        return db.query(UserInfo).filter(UserInfo.nick_name == nick_name).first()

    def get_by_email_and_password(self, db: Session, email: str, password: str) -> Optional[UserInfo]:
        """Get user by email and password"""
        return db.query(UserInfo).filter(
            UserInfo.email == email,
            UserInfo.password == password
        ).first()

    def create(self, db: Session, obj_in: Dict[str, Any]) -> UserInfo:
        """Create a new user"""
        db_obj = UserInfo(
            user_id=obj_in.get("user_id"),
            nick_name=obj_in.get("nick_name"),
            email=obj_in.get("email"),
            password=obj_in.get("password"),
            sex=obj_in.get("sex"),
            person_description=obj_in.get("person_description", ""),
            join_time=obj_in.get("join_time", datetime.now()),
            last_login_time=obj_in.get("join_time", datetime.now()),
            last_login_ip=obj_in.get("last_login_ip", ""),
            last_login_ip_address=obj_in.get("last_login_ip_address", ""),
            total_integral=obj_in.get("total_integral", 0),
            current_integral=obj_in.get("current_integral", 0),
            status=obj_in.get("status", 1),
            is_admin=obj_in.get("is_admin", 0),
            image=obj_in.get("image", obj_in.get("user_id"))
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: UserInfo, obj_in: Union[Dict[str, Any], Any]) -> UserInfo:
        """Update user"""
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)

        for field in update_data:
            if hasattr(db_obj, field) and field != "user_id":
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_last_login(self, db: Session, user: UserInfo, ip: str, ip_address: str) -> UserInfo:
        """Update user's last login information"""
        user.last_login_time = datetime.now()
        user.last_login_ip = ip
        user.last_login_ip_address = ip_address

        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def add_integral(self, db: Session, user_id: str, oper_type: int, integral: int) -> UserIntegralRecord:
        """Add integral record and update user's integral"""
        # Create integral record
        record = UserIntegralRecord(
            user_id=user_id,
            oper_type=oper_type,
            integral=integral,
            create_time=datetime.now()
        )

        # Update user's integral
        user = self.get_by_user_id(db, user_id)
        if user:
            user.total_integral = user.total_integral + integral
            user.current_integral = user.current_integral + integral

            db.add(record)
            db.add(user)
            db.commit()
            db.refresh(record)

            return record
        return None

    def save_email_code(self, db: Session, email: str, code: str) -> EmailCode:
        """Save email verification code"""
        # Check if there's an existing code
        existing_code = db.query(EmailCode).filter(EmailCode.email == email).first()

        if existing_code:
            existing_code.code = code
            existing_code.create_time = datetime.now()
            existing_code.status = False
            db_obj = existing_code
        else:
            db_obj = EmailCode(
                email=email,
                code=code,
                create_time=datetime.now(),
                status=False
            )
            db.add(db_obj)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def verify_email_code(self, db: Session, email: str, code: str) -> bool:
        """Verify email verification code"""
        code_obj = db.query(EmailCode).filter(
            EmailCode.email == email,
            EmailCode.code == code,
            EmailCode.status == False
        ).first()

        if code_obj:
            code_obj.status = True
            db.add(code_obj)
            db.commit()
            return True
        return False


user_repository = UserRepository()