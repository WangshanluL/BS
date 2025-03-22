from typing import Dict, Any, Optional, List, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from app.db.models.chat import MasterChat, MasterMessage
from datetime import datetime
import json

class MasterChatRepository:
    async def get_by_id(self, db: AsyncSession, id: int) -> Optional[MasterChat]:
        """Get chat by id"""
        result = await db.execute(select(MasterChat).filter(MasterChat.id == id))
        return result.scalars().first()

    async def get_by_chat_id(self, db: AsyncSession, chat_id: str) -> Optional[MasterChat]:
        """Get chat by chat_id"""
        result = await db.execute(select(MasterChat).filter(MasterChat.chat_id == chat_id))
        return result.scalars().first()

    async def get_by_user_id(self, db: AsyncSession, user_id: str) -> List[MasterChat]:
        """Get all chats for a user"""
        result = await db.execute(select(MasterChat).filter(MasterChat.user_id == user_id))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: Dict[str, Any]) -> MasterChat:
        """Create a new chat"""
        db_obj = MasterChat(
            chat_id=obj_in.get("chat_id"),
            title=obj_in.get("title"),
            user_id=obj_in.get("user_id"),
            created_time=obj_in.get("created_time", datetime.now())
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, db_obj: MasterChat, obj_in: Union[Dict[str, Any], Any]) -> MasterChat:
        """Update chat"""
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)

        for field in update_data:
            if hasattr(db_obj, field) and field != "chat_id" and field != "id":
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, chat_id: str) -> None:
        """Delete chat"""
        db_obj = await self.get_by_chat_id(db, chat_id)
        if db_obj:
            await db.delete(db_obj)
            await db.commit()


class MasterMessageRepository:
    async def get_by_id(self, db: AsyncSession, id: int) -> Optional[MasterMessage]:
        """Get message by id"""
        result = await db.execute(select(MasterMessage).filter(MasterMessage.id == id))
        return result.scalars().first()

    async def get_by_chat_id(self, db: AsyncSession, chat_id: str) -> List[MasterMessage]:
        """Get all messages for a chat"""
        result = await db.execute(select(MasterMessage).filter(MasterMessage.chat_id == chat_id))
        return result.scalars().all()

    async def get_by_user_id(self, db: AsyncSession, user_id: str) -> List[MasterMessage]:
        """Get all messages for a user"""
        result = await db.execute(select(MasterMessage).filter(MasterMessage.user_id == user_id))
        return result.scalars().all()

    async def get_by_chat_id_and_user_id(self, db: AsyncSession, chat_id: str, user_id: str) -> List[MasterMessage]:
        """Get all messages for a chat and user"""
        result = await db.execute(
            select(MasterMessage).filter(
                MasterMessage.chat_id == chat_id,
                MasterMessage.user_id == user_id
            )
        )
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: Dict[str, Any]) -> MasterMessage:
        """Create a new message"""
        web_reference = obj_in.get("web_reference")
        gene_reference = obj_in.get("gene_reference")
        relevant_topics = obj_in.get("relevant_topics")

        # 将复杂类型转换为JSON字符串
        if web_reference is not None and not isinstance(web_reference, str):
            web_reference = json.dumps(web_reference)

        if gene_reference is not None and not isinstance(gene_reference, str):
            gene_reference = json.dumps(gene_reference)

        if relevant_topics is not None and not isinstance(relevant_topics, str):
            relevant_topics = json.dumps(relevant_topics)

        db_obj = MasterMessage(
            role=obj_in.get("role"),
            content=obj_in.get("content"),
            web_reference=web_reference,
            relevant_topics=relevant_topics,
            gene_reference=gene_reference,
            user_id=obj_in.get("user_id"),
            chat_id=obj_in.get("chat_id"),
            created_time=obj_in.get("created_time", datetime.now())
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, db_obj: MasterMessage,
                     obj_in: Union[Dict[str, Any], Any]) -> MasterMessage:
        """Update message"""
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)

        for field in update_data:
            if hasattr(db_obj, field) and field != "id":
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, id: int) -> None:
        """Delete message"""
        db_obj = await self.get_by_id(db, id)
        if db_obj:
            await db.delete(db_obj)
            await db.commit()

    async def delete_by_chat_id(self, db: AsyncSession, chat_id: str) -> None:
        """Delete all messages for a chat"""
        stmt = delete(MasterMessage).where(MasterMessage.chat_id == chat_id)
        await db.execute(stmt)
        await db.commit()

    async def get_message_by_chat_id_and_rerank(self, db: AsyncSession, chat_id: str) -> List[MasterMessage]:
        """Get all messages for a chat ordered by created_time"""
        result = await db.execute(
            select(MasterMessage)
            .filter(MasterMessage.chat_id == chat_id)
            .order_by(MasterMessage.created_time.asc())
        )
        return result.scalars().all()


master_chat_repository = MasterChatRepository()
master_message_repository = MasterMessageRepository()