from typing import Optional,List,Any,Dict
from pydantic import BaseModel, EmailStr, validator, Field
from datetime import datetime
class GetHistoryRequest(BaseModel):
    chat_id: str
    user_id: str

class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    web_reference: Optional[Any] = None
    gene_reference: Optional[Any] = None
    relevant_topics: Optional[Any] = None
    created_time: datetime


class ChatHistoryResponse(BaseModel):
    chat_id: str
    title: str
    messages: List[MessageResponse]
    total_messages: int
#
# class CreateMasterMessage(BaseModel):
#     role: str
#     content: str
#     chat_id:str
#     user_id:str
#     web_reference: Optional[Any] = None
#     gene_reference: Optional[Any] = None
#     relevant_topics : Optional[Any] = None
#     create_time: Optional[datetime] = None
import json


class CreateMasterMessage(BaseModel):
    role: str
    content: str
    chat_id: str
    user_id: str
    web_reference: Optional[Any] = None
    gene_reference: Optional[Any] = None
    relevant_topics: Optional[Any] = None
    create_time: Optional[datetime] = None

    # def to_db_dict(self) -> Dict[str, Any]:
    #     """转换为数据库可用的字典"""
    #     result = self.model_dump()  # 使用model_dump()替代dict()
    #     # 转换复杂类型为JSON字符串
    #     for field in ['web_reference', 'gene_reference', 'relevant_topics']:
    #         if result[field] is not None and not isinstance(result[field], str):
    #             result[field] = json.dumps(result[field])
    #     return result
class CreateNewChat(BaseModel):
    user_id : str
class GetUserChats(BaseModel):
    user_id : str
class UpdateAccessTimeRequest(BaseModel):
    chat_id : str
    user_id : str