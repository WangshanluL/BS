import asyncio
from neo4j import AsyncDriver
from app.db.db_neo4j import async_neo4j_driver

async def fetch_concept_nodes(driver: AsyncDriver):
    query = """
    MATCH (n:ConceptNode)
    RETURN n.concept_name AS concept_name, n.description AS description
    """
    concept_list = []  # 存储结果的列表
    try:
        async with driver.session() as session:
            result = await session.run(query)

            async for record in result:  # 逐行获取数据
                concept_name = record["concept_name"] or ""
                description = record["description"] or ""
                concept_list.append(f"{concept_name}:{description}")  # 组成字符串

    except Exception as e:
        print(f"Error fetching concept nodes: {e}")

    return concept_list  # 返回列表

async def main():
    concept_nodes = await fetch_concept_nodes(async_neo4j_driver)

    with open("output.txt", "w", encoding="utf-8") as file:
        for line in concept_nodes:
            file.write(line + "\n")

    print("文件已成功保存为 output.txt")
    #print(concept_nodes)  # 直接打印查看

if __name__ == "__main__":
    asyncio.run(main())
