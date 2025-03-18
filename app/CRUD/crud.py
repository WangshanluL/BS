# crud.py
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime
from typing import List, Optional, Dict, Any, Union

# Import your models
from app.db.models import (
    UserInfo, MasterChat, MasterMessage, EmailCode, ForumBoard,
    ForumArticle, ForumArticleAttachment, ForumArticleAttachmentDownload,
    ForumComment, LikeRecord, SysSetting, UserIntegralRecord, UserMessage
)


# === UserInfo CRUD operations ===

def create_user(db: Session, user_data: Dict[str, Any]) -> UserInfo:
    """Create a new user."""
    user = UserInfo(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: str) -> Optional[UserInfo]:
    """Get a user by ID."""
    return db.query(UserInfo).filter(UserInfo.user_id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[UserInfo]:
    """Get a user by email."""
    return db.query(UserInfo).filter(UserInfo.email == email).first()


def get_user_by_nickname(db: Session, nick_name: str) -> Optional[UserInfo]:
    """Get a user by nickname."""
    return db.query(UserInfo).filter(UserInfo.nick_name == nick_name).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[UserInfo]:
    """Get a list of users with pagination."""
    return db.query(UserInfo).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: str, user_data: Dict[str, Any]) -> Optional[UserInfo]:
    """Update a user."""
    user = get_user(db, user_id)
    if user:
        for key, value in user_data.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
    return user


def delete_user(db: Session, user_id: str) -> bool:
    """Delete a user."""
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False


def update_user_login_info(db: Session, user_id: str, ip: str, ip_address: str) -> bool:
    """Update a user's login information."""
    user = get_user(db, user_id)
    if user:
        user.last_login_time = datetime.now()
        user.last_login_ip = ip
        user.last_login_ip_address = ip_address
        db.commit()
        return True
    return False


# === MasterChat CRUD operations ===

def create_chat(db: Session, chat_data: Dict[str, Any]) -> MasterChat:
    """Create a new chat."""
    chat = MasterChat(**chat_data)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


def get_chat(db: Session, chat_id: str) -> Optional[MasterChat]:
    """Get a chat by chat_id."""
    return db.query(MasterChat).filter(MasterChat.chat_id == chat_id).first()


def get_chats_by_user(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[MasterChat]:
    """Get chats for a specific user."""
    return db.query(MasterChat).filter(
        MasterChat.user_id == user_id
    ).order_by(MasterChat.created_time.desc()).offset(skip).limit(limit).all()


def update_chat(db: Session, chat_id: str, chat_data: Dict[str, Any]) -> Optional[MasterChat]:
    """Update a chat."""
    chat = get_chat(db, chat_id)
    if chat:
        for key, value in chat_data.items():
            setattr(chat, key, value)
        db.commit()
        db.refresh(chat)
    return chat


def delete_chat(db: Session, chat_id: str) -> bool:
    """Delete a chat."""
    chat = get_chat(db, chat_id)
    if chat:
        db.delete(chat)
        db.commit()
        return True
    return False


# === MasterMessage CRUD operations ===

def create_message(db: Session, message_data: Dict[str, Any]) -> MasterMessage:
    """Create a new message."""
    message = MasterMessage(**message_data)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_message(db: Session, message_id: int) -> Optional[MasterMessage]:
    """Get a message by ID."""
    return db.query(MasterMessage).filter(MasterMessage.id == message_id).first()


def get_messages_by_chat(db: Session, chat_id: str) -> List[MasterMessage]:
    """Get all messages for a specific chat."""
    return db.query(MasterMessage).filter(
        MasterMessage.chat_id == chat_id
    ).order_by(MasterMessage.created_time).all()


def update_message(db: Session, message_id: int, message_data: Dict[str, Any]) -> Optional[MasterMessage]:
    """Update a message."""
    message = get_message(db, message_id)
    if message:
        for key, value in message_data.items():
            setattr(message, key, value)
        db.commit()
        db.refresh(message)
    return message


def delete_message(db: Session, message_id: int) -> bool:
    """Delete a message."""
    message = get_message(db, message_id)
    if message:
        db.delete(message)
        db.commit()
        return True
    return False


# === EmailCode CRUD operations ===

def create_email_code(db: Session, email: str, code: str) -> EmailCode:
    """Create a new email verification code."""
    email_code = EmailCode(email=email, code=code)
    db.add(email_code)
    db.commit()
    db.refresh(email_code)
    return email_code


def get_email_code(db: Session, email: str, code: str) -> Optional[EmailCode]:
    """Get an email code."""
    return db.query(EmailCode).filter(
        EmailCode.email == email,
        EmailCode.code == code,
        EmailCode.status == False
    ).first()


def mark_email_code_used(db: Session, email: str, code: str) -> bool:
    """Mark an email code as used."""
    email_code = get_email_code(db, email, code)
    if email_code:
        email_code.status = True
        db.commit()
        return True
    return False


# === ForumBoard CRUD operations ===

def create_board(db: Session, board_data: Dict[str, Any]) -> ForumBoard:
    """Create a new forum board."""
    board = ForumBoard(**board_data)
    db.add(board)
    db.commit()
    db.refresh(board)
    return board


def get_board(db: Session, board_id: int) -> Optional[ForumBoard]:
    """Get a board by ID."""
    return db.query(ForumBoard).filter(ForumBoard.board_id == board_id).first()


def get_boards(db: Session, p_board_id: Optional[int] = None) -> List[ForumBoard]:
    """Get all boards, optionally filtered by parent board ID."""
    query = db.query(ForumBoard)
    if p_board_id is not None:
        query = query.filter(ForumBoard.p_board_id == p_board_id)
    return query.order_by(ForumBoard.sort).all()


def update_board(db: Session, board_id: int, board_data: Dict[str, Any]) -> Optional[ForumBoard]:
    """Update a board."""
    board = get_board(db, board_id)
    if board:
        for key, value in board_data.items():
            setattr(board, key, value)
        db.commit()
        db.refresh(board)
    return board


def delete_board(db: Session, board_id: int) -> bool:
    """Delete a board."""
    board = get_board(db, board_id)
    if board:
        db.delete(board)
        db.commit()
        return True
    return False


# === ForumArticle CRUD operations ===

def create_article(db: Session, article_data: Dict[str, Any]) -> ForumArticle:
    """Create a new forum article."""
    article = ForumArticle(**article_data)
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


def get_article(db: Session, article_id: str) -> Optional[ForumArticle]:
    """Get an article by ID."""
    return db.query(ForumArticle).filter(ForumArticle.article_id == article_id).first()


def get_articles(db: Session, board_id: Optional[int] = None,
                 user_id: Optional[str] = None,
                 status: Optional[int] = 1,
                 skip: int = 0, limit: int = 20) -> List[ForumArticle]:
    """Get articles with various filters."""
    query = db.query(ForumArticle)

    if board_id is not None:
        query = query.filter(ForumArticle.board_id == board_id)

    if user_id is not None:
        query = query.filter(ForumArticle.user_id == user_id)

    if status is not None:
        query = query.filter(ForumArticle.status == status)

    return query.order_by(
        ForumArticle.top_type.desc(),
        ForumArticle.post_time.desc()
    ).offset(skip).limit(limit).all()


def update_article(db: Session, article_id: str, article_data: Dict[str, Any]) -> Optional[ForumArticle]:
    """Update an article."""
    article = get_article(db, article_id)
    if article:
        for key, value in article_data.items():
            setattr(article, key, value)
        db.commit()
        db.refresh(article)
    return article


def delete_article(db: Session, article_id: str) -> bool:
    """Mark an article as deleted."""
    article = get_article(db, article_id)
    if article:
        article.status = -1
        db.commit()
        return True
    return False


def hard_delete_article(db: Session, article_id: str) -> bool:
    """Physically delete an article."""
    article = get_article(db, article_id)
    if article:
        db.delete(article)
        db.commit()
        return True
    return False


def increment_article_view(db: Session, article_id: str) -> bool:
    """Increment an article's view count."""
    article = get_article(db, article_id)
    if article:
        article.read_count += 1
        db.commit()
        return True
    return False


# === ForumComment CRUD operations ===

def create_comment(db: Session, comment_data: Dict[str, Any]) -> ForumComment:
    """Create a new comment."""
    comment = ForumComment(**comment_data)
    db.add(comment)

    # Increment the article's comment count
    article = get_article(db, comment_data["article_id"])
    if article:
        article.comment_count += 1

    db.commit()
    db.refresh(comment)
    return comment


def get_comment(db: Session, comment_id: int) -> Optional[ForumComment]:
    """Get a comment by ID."""
    return db.query(ForumComment).filter(ForumComment.comment_id == comment_id).first()


def get_comments_by_article(db: Session, article_id: str, status: int = 1,
                            skip: int = 0, limit: int = 50) -> List[ForumComment]:
    """Get comments for a specific article."""
    return db.query(ForumComment).filter(
        ForumComment.article_id == article_id,
        ForumComment.status == status
    ).order_by(
        ForumComment.top_type.desc(),
        ForumComment.post_time.desc()
    ).offset(skip).limit(limit).all()


def update_comment(db: Session, comment_id: int, comment_data: Dict[str, Any]) -> Optional[ForumComment]:
    """Update a comment."""
    comment = get_comment(db, comment_id)
    if comment:
        for key, value in comment_data.items():
            setattr(comment, key, value)
        db.commit()
        db.refresh(comment)
    return comment


def delete_comment(db: Session, comment_id: int) -> bool:
    """Delete a comment."""
    comment = get_comment(db, comment_id)
    if comment:
        # Decrement the article's comment count
        article = get_article(db, comment.article_id)
        if article:
            article.comment_count = max(0, article.comment_count - 1)

        db.delete(comment)
        db.commit()
        return True
    return False


# === LikeRecord CRUD operations ===

def create_like(db: Session, op_type: int, object_id: str,
                user_id: str, author_user_id: str) -> Union[LikeRecord, bool]:
    """Create a new like record."""
    # Check if like already exists
    existing_like = db.query(LikeRecord).filter(
        LikeRecord.op_type == op_type,
        LikeRecord.object_id == object_id,
        LikeRecord.user_id == user_id
    ).first()

    if existing_like:
        return False

    like = LikeRecord(
        op_type=op_type,
        object_id=object_id,
        user_id=user_id,
        author_user_id=author_user_id
    )
    db.add(like)

    # Update good_count for the liked object
    if op_type == 0:  # Article like
        article = get_article(db, object_id)
        if article:
            article.good_count += 1
    elif op_type == 1:  # Comment like
        comment = get_comment(db, int(object_id))
        if comment:
            comment.good_count += 1

    db.commit()
    db.refresh(like)
    return like


def get_like(db: Session, op_type: int, object_id: str, user_id: str) -> Optional[LikeRecord]:
    """Get a like record."""
    return db.query(LikeRecord).filter(
        LikeRecord.op_type == op_type,
        LikeRecord.object_id == object_id,
        LikeRecord.user_id == user_id
    ).first()


def delete_like(db: Session, op_type: int, object_id: str, user_id: str) -> bool:
    """Delete a like record."""
    like = get_like(db, op_type, object_id, user_id)
    if like:
        # Update good_count for the liked object
        if op_type == 0:  # Article like
            article = get_article(db, object_id)
            if article:
                article.good_count = max(0, article.good_count - 1)
        elif op_type == 1:  # Comment like
            comment = get_comment(db, int(object_id))
            if comment:
                comment.good_count = max(0, comment.good_count - 1)

        db.delete(like)
        db.commit()
        return True
    return False


# === UserIntegralRecord CRUD operations ===

def create_integral_record(db: Session, user_id: str, oper_type: int, integral: int) -> UserIntegralRecord:
    """Create a new integral record and update user integral."""
    record = UserIntegralRecord(
        user_id=user_id,
        oper_type=oper_type,
        integral=integral
    )
    db.add(record)

    # Update user's integral
    user = get_user(db, user_id)
    if user:
        user.total_integral += integral
        user.current_integral += integral

    db.commit()
    db.refresh(record)
    return record


def get_integral_records(db: Session, user_id: str, skip: int = 0, limit: int = 50) -> List[UserIntegralRecord]:
    """Get integral records for a user."""
    return db.query(UserIntegralRecord).filter(
        UserIntegralRecord.user_id == user_id
    ).order_by(UserIntegralRecord.create_time.desc()).offset(skip).limit(limit).all()


# === UserMessage CRUD operations ===

def create_message_notification(db: Session, message_data: Dict[str, Any]) -> Optional[UserMessage]:
    """Create a new message notification."""
    # Check for duplicates using unique constraint
    existing_message = None
    if all(k in message_data for k in ["article_id", "comment_id", "send_user_id", "message_type"]):
        existing_message = db.query(UserMessage).filter(
            UserMessage.article_id == message_data["article_id"],
            UserMessage.comment_id == message_data["comment_id"],
            UserMessage.send_user_id == message_data["send_user_id"],
            UserMessage.message_type == message_data["message_type"]
        ).first()

    if existing_message:
        return None

    message = UserMessage(**message_data)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_user_messages(db: Session, user_id: str, status: Optional[int] = None,
                      skip: int = 0, limit: int = 50) -> List[UserMessage]:
    """Get messages for a user."""
    query = db.query(UserMessage).filter(UserMessage.received_user_id == user_id)

    if status is not None:
        query = query.filter(UserMessage.status == status)

    return query.order_by(UserMessage.create_time.desc()).offset(skip).limit(limit).all()


def mark_message_read(db: Session, message_id: int) -> bool:
    """Mark a message as read."""
    message = db.query(UserMessage).filter(UserMessage.message_id == message_id).first()
    if message:
        message.status = 2  # Read status
        db.commit()
        return True
    return False


def mark_all_messages_read(db: Session, user_id: str) -> int:
    """Mark all messages for a user as read."""
    result = db.query(UserMessage).filter(
        UserMessage.received_user_id == user_id,
        UserMessage.status == 1
    ).update({"status": 2})
    db.commit()
    return result


def delete_message(db: Session, message_id: int) -> bool:
    """Delete a message."""
    message = db.query(UserMessage).filter(UserMessage.message_id == message_id).first()
    if message:
        db.delete(message)
        db.commit()
        return True
    return False


# === ForumArticleAttachment CRUD operations ===

def create_attachment(db: Session, attachment_data: Dict[str, Any]) -> ForumArticleAttachment:
    """Create a new attachment."""
    attachment = ForumArticleAttachment(**attachment_data)
    db.add(attachment)

    # Update article's attachment status
    article = get_article(db, attachment_data["article_id"])
    if article:
        article.attachment_type = 1

    db.commit()
    db.refresh(attachment)
    return attachment


def get_attachment(db: Session, file_id: str) -> Optional[ForumArticleAttachment]:
    """Get an attachment by ID."""
    return db.query(ForumArticleAttachment).filter(ForumArticleAttachment.file_id == file_id).first()


def get_attachments_by_article(db: Session, article_id: str) -> List[ForumArticleAttachment]:
    """Get all attachments for an article."""
    return db.query(ForumArticleAttachment).filter(
        ForumArticleAttachment.article_id == article_id
    ).all()


def increment_download_count(db: Session, file_id: str) -> bool:
    """Increment an attachment's download count."""
    attachment = get_attachment(db, file_id)
    if attachment:
        attachment.download_count += 1
        db.commit()
        return True
    return False


def delete_attachment(db: Session, file_id: str) -> bool:
    """Delete an attachment."""
    attachment = get_attachment(db, file_id)
    if attachment:
        # Check if this is the last attachment for the article
        attachment_count = db.query(ForumArticleAttachment).filter(
            ForumArticleAttachment.article_id == attachment.article_id
        ).count()

        if attachment_count <= 1:
            # Update article's attachment status
            article = get_article(db, attachment.article_id)
            if article:
                article.attachment_type = 0

        db.delete(attachment)
        db.commit()
        return True
    return False


# === ForumArticleAttachmentDownload CRUD operations ===

def create_attachment_download(db: Session, file_id: str, user_id: str,
                               article_id: str) -> ForumArticleAttachmentDownload:
    """Create or update an attachment download record."""
    download = db.query(ForumArticleAttachmentDownload).filter(
        ForumArticleAttachmentDownload.file_id == file_id,
        ForumArticleAttachmentDownload.user_id == user_id
    ).first()

    if download:
        download.download_count += 1
    else:
        download = ForumArticleAttachmentDownload(
            file_id=file_id,
            user_id=user_id,
            article_id=article_id
        )
        db.add(download)

    # Increment the attachment's download count
    increment_download_count(db, file_id)

    db.commit()
    if download not in db.new:
        db.refresh(download)

    return download


def get_user_downloads(db: Session, user_id: str) -> List[ForumArticleAttachmentDownload]:
    """Get all downloads for a user."""
    return db.query(ForumArticleAttachmentDownload).filter(
        ForumArticleAttachmentDownload.user_id == user_id
    ).all()


# === SysSetting CRUD operations ===

def get_system_setting(db: Session, code: str) -> Optional[SysSetting]:
    """Get a system setting by code."""
    return db.query(SysSetting).filter(SysSetting.code == code).first()


def update_system_setting(db: Session, code: str, json_content: str) -> SysSetting:
    """Update or create a system setting."""
    setting = get_system_setting(db, code)

    if setting:
        setting.json_content = json_content
    else:
        setting = SysSetting(code=code, json_content=json_content)
        db.add(setting)

    db.commit()
    db.refresh(setting)
    return setting


def delete_system_setting(db: Session, code: str) -> bool:
    """Delete a system setting."""
    setting = get_system_setting(db, code)
    if setting:
        db.delete(setting)
        db.commit()
        return True
    return False