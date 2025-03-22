# app.models.models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, BigInteger, Float, \
    UniqueConstraint, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base




class ForumBoard(Base):
    __tablename__ = "forum_board"

    board_id = Column(Integer, primary_key=True, autoincrement=True, comment="板块ID")
    p_board_id = Column(Integer, comment="父级板块ID")
    board_name = Column(String(50), comment="板块名")
    cover = Column(String(50), comment="封面")
    board_desc = Column(String(150), comment="描述")
    sort = Column(Integer, comment="排序")
    post_type = Column(Boolean, default=True, comment="0:只允许管理员发帖 1:任何人可以发帖")

    # Relationships
    articles = relationship("ForumArticle", foreign_keys="ForumArticle.board_id", back_populates="board")
    parent_articles = relationship("ForumArticle", foreign_keys="ForumArticle.p_board_id",
                                   back_populates="parent_board")


class ForumArticle(Base):
    __tablename__ = "forum_article"

    article_id = Column(String(15), primary_key=True, comment="文章ID")
    board_id = Column(Integer, ForeignKey("forum_board.board_id"), comment="板块ID")
    board_name = Column(String(50), comment="板块名称")
    p_board_id = Column(Integer, ForeignKey("forum_board.board_id"), comment="父级板块ID")
    p_board_name = Column(String(50), comment="父板块名称")
    user_id = Column(String(15), ForeignKey("user_info.user_id"), comment="用户ID")
    nick_name = Column(String(20), comment="昵称")
    user_ip_address = Column(String(100), comment="最后登录ip地址")
    title = Column(String(150), comment="标题")
    cover = Column(String(100), comment="封面")
    content = Column(Text, comment="内容")
    markdown_content = Column(Text, comment="markdown内容")
    editor_type = Column(Integer, comment="0:富文本编辑器 1:markdown编辑器")
    summary = Column(String(200), comment="摘要")
    post_time = Column(DateTime, default=datetime.now, comment="发布时间")
    last_update_time = Column(DateTime, onupdate=datetime.now, comment="最后更新时间")
    read_count = Column(Integer, default=0, comment="阅读数量")
    good_count = Column(Integer, default=0, comment="点赞数")
    comment_count = Column(Integer, default=0, comment="评论数")
    top_type = Column(Integer, default=0, comment="0未置顶 1:已置顶")
    attachment_type = Column(Integer, default=0, comment="0:没有附件 1:有附件")
    status = Column(Integer, default=0, comment="-1已删除 0:待审核 1:已审核")

    # Relationships
    board = relationship("ForumBoard", foreign_keys=[board_id], back_populates="articles")
    parent_board = relationship("ForumBoard", foreign_keys=[p_board_id], back_populates="parent_articles")
    user = relationship("UserInfo", back_populates="articles")
    attachments = relationship("ForumArticleAttachment", back_populates="article")
    comments = relationship("ForumComment", back_populates="article")
    messages = relationship("UserMessage", back_populates="article")


class ForumArticleAttachment(Base):
    __tablename__ = "forum_article_attachment"

    file_id = Column(String(15), primary_key=True, comment="文件ID")
    article_id = Column(String(15), ForeignKey("forum_article.article_id"), comment="文章ID")
    user_id = Column(String(15), ForeignKey("user_info.user_id"), comment="用户id")
    file_size = Column(BigInteger, comment="文件大小")
    file_name = Column(String(200), comment="文件名称")
    download_count = Column(Integer, default=0, comment="下载次数")
    file_path = Column(String(100), comment="文件路径")
    file_type = Column(Integer, comment="文件类型")
    integral = Column(Integer, default=0, comment="下载所需积分")

    # Relationships
    article = relationship("ForumArticle", back_populates="attachments")
    downloads = relationship("ForumArticleAttachmentDownload", back_populates="attachment")


class ForumArticleAttachmentDownload(Base):
    __tablename__ = "forum_article_attachment_download"

    file_id = Column(String(15), ForeignKey("forum_article_attachment.file_id"), primary_key=True, comment="文件ID")
    user_id = Column(String(15), ForeignKey("user_info.user_id"), primary_key=True, comment="用户id")
    article_id = Column(String(15), ForeignKey("forum_article.article_id"), comment="文章ID")
    download_count = Column(Integer, default=1, comment="文件下载次数")

    # Relationships
    attachment = relationship("ForumArticleAttachment", back_populates="downloads")


class ForumComment(Base):
    __tablename__ = "forum_comment"

    comment_id = Column(Integer, primary_key=True, autoincrement=True, comment="评论ID")
    p_comment_id = Column(Integer, comment="父级评论ID")
    article_id = Column(String(15), ForeignKey("forum_article.article_id"), comment="文章ID")
    content = Column(String(800), comment="回复内容")
    img_path = Column(String(150), comment="图片")
    user_id = Column(String(15), ForeignKey("user_info.user_id"), comment="用户ID")
    nick_name = Column(String(20), comment="昵称")
    user_ip_address = Column(String(100), comment="用户ip地址")
    reply_user_id = Column(String(15), comment="回复人ID")
    reply_nick_name = Column(String(20), comment="回复人昵称")
    top_type = Column(Integer, default=0, comment="0:未置顶 1:置顶")
    post_time = Column(DateTime, default=datetime.now, comment="发布时间")
    good_count = Column(Integer, default=0, comment="good数量")
    status = Column(Integer, default=0, comment="0:待审核 1:已审核")

    # Relationships
    article = relationship("ForumArticle", back_populates="comments")
    user = relationship("UserInfo", back_populates="comments")


class LikeRecord(Base):
    __tablename__ = "like_record"

    op_id = Column(Integer, primary_key=True, autoincrement=True, comment="自增ID")
    op_type = Column(Integer, comment="操作类型0:文章点赞 1:评论点赞")
    object_id = Column(String(15), comment="主体ID")
    user_id = Column(String(15), ForeignKey("user_info.user_id"), comment="用户ID")
    create_time = Column(DateTime, default=datetime.now, comment="发布时间")
    author_user_id = Column(String(15), comment="主体作者ID")

    __table_args__ = (
        UniqueConstraint('object_id', 'user_id', 'op_type', name='idx_key'),
    )


class SysSetting(Base):
    __tablename__ = "sys_setting"

    code = Column(String(10), primary_key=True, comment="编号")
    json_content = Column(String(500), comment="设置信息")

class UserMessage(Base):
    __tablename__ = "user_message"

    message_id = Column(Integer, primary_key=True, autoincrement=True, comment="自增ID")
    received_user_id = Column(String(15), ForeignKey("user_info.user_id"), comment="接收人用户ID")
    article_id = Column(String(15), ForeignKey("forum_article.article_id"), comment="文章ID")
    article_title = Column(String(150), comment="文章标题")
    comment_id = Column(Integer, comment="评论ID")
    send_user_id = Column(String(15), ForeignKey("user_info.user_id"), comment="发送人用户ID")
    send_nick_name = Column(String(20), comment="发送人昵称")
    message_type = Column(Integer, comment="0:系统消息 1:评论 2:文章点赞 3:评论点赞 4:附件下载")
    message_content = Column(String(1000), comment="消息内容")
    status = Column(Integer, default=1, comment="1:未读 2:已读")
    create_time = Column(DateTime, default=datetime.now, comment="创建时间")

    # Relationships
    received_user = relationship("UserInfo", foreign_keys=[received_user_id], back_populates="received_messages")
    send_user = relationship("UserInfo", foreign_keys=[send_user_id], back_populates="sent_messages")
    article = relationship("ForumArticle", back_populates="messages")

    __table_args__ = (
        UniqueConstraint('article_id', 'comment_id', 'send_user_id', 'message_type', name='idx_key'),
    )

