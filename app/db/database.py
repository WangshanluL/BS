from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.core.config import settings

# 异步数据库连接URL (注意driver前缀改为aiomysql)
DATABASE_URL = f"mysql+aiomysql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DATABASE}?charset=utf8mb4"

# 创建异步引擎
engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=20,
    max_overflow=20,
    echo=False
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

# 模型基类
Base = declarative_base()

# 异步上下文管理器
async def get_db():
    """异步上下文管理器版本"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e

# FastAPI依赖项
async def get_db_session():
    """FastAPI异步依赖项"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

