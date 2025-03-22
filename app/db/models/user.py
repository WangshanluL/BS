from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class UserInfo(Base):
    __tablename__ = "user_info"

    user_id = Column(String(15), primary_key=True, comment="用户ID")
    nick_name = Column(String(20), unique=True, comment="昵称")
    email = Column(String(150), unique=True, comment="邮箱")
    password = Column(String(50), comment="密码")
    sex = Column(Integer, comment="0:女 1:男")
    person_description = Column(String(200), comment="个人描述")
    join_time = Column(DateTime, default=datetime.now, comment="加入时间")
    last_login_time = Column(DateTime, comment="最后登录时间")
    last_login_ip = Column(String(15), comment="最后登录IP")
    last_login_ip_address = Column(String(100), comment="最后登录ip地址")
    total_integral = Column(Integer, default=0, comment="积分")
    current_integral = Column(Integer, default=0, comment="当前积分")
    status = Column(Integer, default=1, comment="0:禁用 1:正常")
    is_admin = Column(Integer, default=0)
    image = Column(String(255))

    # Relationships
    chats = relationship("MasterChat", back_populates="user")
    messages = relationship("MasterMessage", back_populates="user")
    articles = relationship("ForumArticle", back_populates="user")
    comments = relationship("ForumComment", back_populates="user")
    integral_records = relationship("UserIntegralRecord", back_populates="user")
    received_messages = relationship("UserMessage", foreign_keys="UserMessage.received_user_id",
                                    back_populates="received_user")
    sent_messages = relationship("UserMessage", foreign_keys="UserMessage.send_user_id",
                                back_populates="send_user")


class EmailCode(Base):
    __tablename__ = "email_code"

    email = Column(String(150), primary_key=True, comment="邮箱")
    code = Column(String(5), primary_key=True, comment="编号")
    create_time = Column(DateTime, default=datetime.now, comment="创建时间")
    status = Column(Boolean, default=False, comment="0:未使用 1:已使用")


class UserIntegralRecord(Base):
    __tablename__ = "user_integral_record"

    record_id = Column(Integer, primary_key=True, autoincrement=True, comment="记录ID")
    user_id = Column(String(15), ForeignKey("user_info.user_id"), comment="用户ID")
    oper_type = Column(Integer, comment="操作类型")
    integral = Column(Integer, comment="积分")
    create_time = Column(DateTime, default=datetime.now, comment="创建时间")

    # Relationships
    user = relationship("UserInfo", back_populates="integral_records")