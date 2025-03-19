from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.utils.ai_client import client
from app.core.log_config import logger
from app.db.database import get_db
from app.models.models import MasterChat, UserInfo
import json

router = APIRouter(prefix="/chat")


# Pydantic model for chat history response
class ChatHistoryResponse(BaseModel):
    chat_id: str
    title: str


@router.get("/chat-history/{user_id}", response_model=List[ChatHistoryResponse])
async def get_chat_history(user_id: str, db: Session = Depends(get_db)):
    """
    Retrieve chat history for a specific user by user_id.
    Returns a list of chat_id and title for each chat.
    """
    try:
        # Check if user exists
        user = db.query(UserInfo).filter(UserInfo.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Query chats for the user
        chats = db.query(MasterChat).filter(
            MasterChat.user_id == user_id
        ).order_by(MasterChat.created_time.desc()).all()

        # Format the response
        chat_history = [
            {"chat_id": chat.chat_id, "title": chat.title}
            for chat in chats
        ]

        logger.info(f"Retrieved {len(chat_history)} chat history records for user {user_id}")
        return chat_history

    except Exception as e:
        logger.error(f"Error retrieving chat history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving chat history: {str(e)}")