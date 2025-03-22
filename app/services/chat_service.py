from typing import Dict, Any, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.chat_repository import master_chat_repository, master_message_repository
from app.db.models.chat import MasterChat, MasterMessage
import uuid
from datetime import datetime


class MasterChatService:
    async def get_chat(self, db: AsyncSession, chat_id: str) -> Optional[MasterChat]:
        """Get a chat by chat_id"""
        return await master_chat_repository.get_by_chat_id(db, chat_id)

    async def get_user_chats(self, db: AsyncSession, user_id: str) -> List[MasterChat]:
        """Get all chats for a user"""
        return await master_chat_repository.get_by_user_id(db, user_id)

    async def create_chat(self, db: AsyncSession, user_id: str, title: str = None) -> MasterChat:
        """Create a new chat for a user"""
        chat_data = {
            "chat_id": str(uuid.uuid4()),
            "title": title or "New Chat",
            "user_id": user_id,
            "created_time": datetime.now()
        }
        return await master_chat_repository.create(db, chat_data)

    async def update_chat_title(self, db: AsyncSession, chat_id: str, new_title: str) -> Optional[MasterChat]:
        """Update the title of a chat"""
        chat = await master_chat_repository.get_by_chat_id(db, chat_id)
        if not chat:
            return None

        update_data = {"title": new_title}
        return await master_chat_repository.update(db, chat, update_data)

    async def delete_chat(self, db: AsyncSession, chat_id: str) -> bool:
        """Delete a chat and its messages"""
        chat = await master_chat_repository.get_by_chat_id(db, chat_id)
        if not chat:
            return False

        # Delete all messages in the chat first
        await master_message_repository.delete_by_chat_id(db, chat_id)

        # Then delete the chat itself
        await master_chat_repository.delete(db, chat_id)
        return True


master_chat_service = MasterChatService()


class MasterMessageService:
    async def get_chat_messages(self, db: AsyncSession, chat_id: str) -> List[MasterMessage]:
        """Get all messages in a chat"""
        return await master_message_repository.get_by_chat_id(db, chat_id)

    async def get_user_messages(self, db: AsyncSession, user_id: str) -> List[MasterMessage]:
        """Get all messages for a user"""
        return await master_message_repository.get_by_user_id(db, user_id)

    async def update_message_content(self, db: AsyncSession, message_id: int, new_content: str) -> Optional[MasterMessage]:
        """Update the content of a message"""
        message = await master_message_repository.get_by_id(db, message_id)
        if not message:
            return None

        update_data = {"content": new_content}
        return await master_message_repository.update(db, message, update_data)

    async def update_message_references(
            self,
            db: AsyncSession,
            message_id: int,
            web_reference: str = None,
            gene_reference: str = None,
            relevant_topics: str = None
    ) -> Optional[MasterMessage]:
        """Update the references of a message"""
        message = await master_message_repository.get_by_id(db, message_id)
        if not message:
            return None

        update_data = {}
        if web_reference is not None:
            update_data["web_reference"] = web_reference
        if gene_reference is not None:
            update_data["gene_reference"] = gene_reference
        if relevant_topics is not None:
            update_data["relevant_topics"] = relevant_topics
        return await master_message_repository.update(db, message, update_data)

    async def delete_message(self, db: AsyncSession, message_id: int) -> bool:
        """Delete a message"""
        message = await master_message_repository.get_by_id(db, message_id)
        if not message:
            return False

        await master_message_repository.delete(db, message_id)
        return True


from app.schemas.standardResponse import StandardResponse
from app.schemas.chatSchema import MessageResponse, ChatHistoryResponse, CreateMasterMessage


# 创建服务类
class ChatHistoryService:
    async def get_chat_history(self, db: AsyncSession, chat_id: str, user_id: str) -> StandardResponse:
        """
        获取聊天历史记录

        1. 验证聊天所有权
        2. 获取按时间排序的消息
        3. 返回标准格式响应
        """
        # 步骤1: 验证聊天所有权
        chat = await master_chat_repository.get_by_chat_id(db, chat_id)
        if not chat:
            return StandardResponse(code=404, message="Chat not found")

        if chat.user_id != user_id:
            return StandardResponse(code=403, message="You don't have permission to access this chat")

        # 步骤2: 获取消息并按创建时间排序
        messages = await master_message_repository.get_message_by_chat_id_and_rerank(db, chat_id)

        # 步骤3: 构建响应
        message_responses = [
            MessageResponse(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                web_reference=msg.web_reference,
                gene_reference=msg.gene_reference,
                relevant_topics=msg.relevant_topics,
                created_time=msg.created_time
            ) for msg in messages
        ]

        chat_history = ChatHistoryResponse(
            chat_id=chat.chat_id,
            title=chat.title,
            messages=message_responses,
            total_messages=len(message_responses)
        )

        return StandardResponse(
            code=200,
            message="Success",
            data=chat_history
        )

    async def createMasterMessage(self, db: AsyncSession, new_message: CreateMasterMessage):
        """
        创建一个新的master message

        Args:
            db (AsyncSession): 数据库会话
            new_message (CreateMasterMessage): 包含消息数据的模型对象

        Returns:
            MasterMessage: 创建的消息对象
        """
        # 将CreateMasterMessage模型转换为字典
        message_data = {
            "role": new_message.role,
            "content": new_message.content,
            "chat_id": new_message.chat_id,
            "user_id": new_message.user_id,
            "web_reference": new_message.web_reference,
            "relevant_topics": new_message.relevant_topics,
            "gene_reference": new_message.gene_reference,
            "created_time": datetime.now()
        }

        # 调用repository的create方法
        return await master_message_repository.create(db, message_data)


# 创建服务实例
chat_history_service = ChatHistoryService()


# Example usage in a FastAPI route
"""
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.master import MasterChatService, MasterMessageService

router = APIRouter()
chat_service = MasterChatService()
message_service = MasterMessageService()

@router.post("/chats/")
async def create_new_chat(user_id: str, title: str = None, db: AsyncSession = Depends(get_db)):
    return await chat_service.create_chat(db, user_id, title)

@router.get("/chats/{chat_id}")
async def get_chat(chat_id: str, db: AsyncSession = Depends(get_db)):
    chat = await chat_service.get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

@router.post("/chats/{chat_id}/messages/")
async def add_message(chat_id: str, user_id: str, content: str, db: AsyncSession = Depends(get_db)):
    # Create user message
    user_message = await message_service.create_user_message(db, user_id, chat_id, content)

    # Generate assistant response (example)
    assistant_response = "This is an assistant response"
    assistant_message = await message_service.create_assistant_message(
        db, user_id, chat_id, assistant_response, 
        web_reference="https://example.com", 
        gene_reference="Some reference data"
    )

    return {
        "user_message": user_message,
        "assistant_message": assistant_message
    }
"""