
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, BigInteger, Float, \
    UniqueConstraint, func
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base



class MasterChat(Base):
    __tablename__ = "master_chat"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="Primary key ID")
    chat_id = Column(String(50), unique=True, comment="Chat identifier")
    title = Column(String(255), nullable=True, comment="Chat title")
    user_id = Column(String(15), ForeignKey("user_info.user_id"), comment="User ID")
    created_time = Column(DateTime, default=datetime.now, comment="Creation time")

    # Relationships
    user = relationship("UserInfo", back_populates="chats")
    messages = relationship("MasterMessage", back_populates="chat")


class MasterMessage(Base):
    __tablename__ = "master_message"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="Primary key ID")
    role = Column(String(20), comment="Message role (user/assistant)")
    content = Column(Text, nullable=True, comment="Message content")
    web_reference = Column(Text, nullable=True, comment="Web references")
    gene_reference = Column(Text, nullable=True, comment="Gene references")
    relevant_topics = Column(Text, nullable=True, comment="Gene references")
    user_id = Column(String(15), ForeignKey("user_info.user_id"), comment="User ID")
    chat_id = Column(String(50), ForeignKey("master_chat.chat_id"), comment="Chat ID")
    created_time = Column(DateTime, default=datetime.now, comment="Creation time")

    # Relationships
    user = relationship("UserInfo", back_populates="messages")
    chat = relationship("MasterChat", back_populates="messages")



