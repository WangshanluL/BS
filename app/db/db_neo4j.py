from neo4j import AsyncDriver, AsyncGraphDatabase
from app.core.config import settings
from app.core.log_config import logger

def create_neo4j_driver(neo4j_uri: str) -> AsyncDriver:
    try:
        # 创建Neo4j驱动
        driver = AsyncGraphDatabase.driver(
            neo4j_uri,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )
        logger.info(f'Neo4j数据库连接成功, 连接地址: {neo4j_uri}')
        return driver
    except Exception as e:
        logger.info('❌ Neo4j数据库连接失败', e)


async_neo4j_driver = create_neo4j_driver(settings.NEO4J_URL)
