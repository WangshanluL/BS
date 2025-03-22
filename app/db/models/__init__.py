# Import all models here for Alembic to detect
from app.db.models.user import UserInfo, EmailCode, UserIntegralRecord
from app.db.models.chat import MasterChat, MasterMessage
from app.db.models.forum import (
    ForumBoard, ForumArticle, ForumArticleAttachment,
    ForumArticleAttachmentDownload, ForumComment, LikeRecord,
    UserMessage
)
