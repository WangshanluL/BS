import json
from neo4j import GraphDatabase

# 连接到Neo4j数据库
def connect_to_neo4j(uri="bolt://localhost:7687", username="neo4j", password="123456789"):
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        print("已连接到Neo4j数据库")
        return driver
    except Exception as e:
        print(f"连接Neo4j失败: {e}")
        return None

# 关闭Neo4j连接的函数
def close_neo4j_connection(driver):
    if driver is not None:
        driver.close()
        print("Neo4j连接已关闭")

# 执行Cypher查询
def run_cypher_query(driver, query, params=None):
    if params is None:
        params = {}
    
    with driver.session() as session:
        try:
            result = session.run(query, params)
            return result
        except Exception as e:
            print(f"查询执行失败: {e}")
            print(f"查询语句: {query}")
            return None

# 清空数据库（可选）
def clean_database(driver):
    query = "MATCH (n) DETACH DELETE n"
    run_cypher_query(driver, query)
    print("数据库已清空")

# 生成创建章节节点的Cypher语句
def generate_chapter_nodes(data):
    statements = []
    
    # 创建章节节点
    create_chapters = "CREATE "
    chapter_statements = []
    
    for chapter_name, chapter_data in data.items():
        description = chapter_data.get("描述", "")
        chapter_statement = f"({chapter_name}:ChapterNode {{chapter_name: \"{chapter_name}\", description: \"{description}\"}})"
        chapter_statements.append(chapter_statement)
    
    create_chapters += ", ".join(chapter_statements) + ";"
    statements.append(create_chapters)
    
    return statements

# 生成创建子章节节点的Cypher语句
def generate_subchapter_nodes(data):
    statements = []
    
    # 创建子章节节点
    create_subchapters = "CREATE "
    subchapter_statements = []
    
    for chapter_name, chapter_data in data.items():
        for subchapter_name, subchapter_data in chapter_data.items():
            # 只处理包含"描述"的字典项，这些是子章节
            if isinstance(subchapter_data, dict) and "描述" in subchapter_data:
                description = subchapter_data.get("描述", "")
                # 替换可能干扰Cypher语句的特殊字符
                safe_subchapter_name = subchapter_name.replace(" ", "_")
                subchapter_statement = f"({safe_subchapter_name}:SubChapterNode {{subchapter_name: \"{subchapter_name}\", description: \"{description}\"}})"
                subchapter_statements.append(subchapter_statement)
    
    if subchapter_statements:
        create_subchapters += ", ".join(subchapter_statements) + ";"
        statements.append(create_subchapters)
    
    return statements

# 生成创建概念节点的Cypher语句
def generate_concept_nodes(data):
    statements = []
    
    # 创建概念节点
    create_concepts = "CREATE "
    concept_statements = []
    
    for chapter_name, chapter_data in data.items():
        for subchapter_name, subchapter_data in chapter_data.items():
            if isinstance(subchapter_data, dict):
                for concept_name, concept_data in subchapter_data.items():
                    # 只处理包含"描述"的字典项，这些是概念
                    if isinstance(concept_data, dict) and "描述" in concept_data:
                        description = concept_data.get("描述", "")
                        # 替换可能干扰Cypher语句的特殊字符
                        safe_concept_name = f"{concept_name}".replace(" ", "_")
                        concept_statement = f"({safe_concept_name}:ConceptNode {{concept_name: \"{concept_name}\", description: \"{description}\"}})"
                        concept_statements.append(concept_statement)
    
    if concept_statements:
        create_concepts += ", ".join(concept_statements) + ";"
        statements.append(create_concepts)
    
    return statements

# 生成章节与子章节之间关系的Cypher语句
def generate_chapter_subchapter_relationships(data):
    statements = []
    
    for chapter_name, chapter_data in data.items():
        # 找出该章节的所有子章节
        subchapters = []
        for subchapter_name, subchapter_data in chapter_data.items():
            if isinstance(subchapter_data, dict) and "描述" in subchapter_data:
                safe_subchapter_name = subchapter_name.replace(" ", "_")
                subchapters.append(safe_subchapter_name)
        
        if subchapters:
            # 创建关系查询
            query = f"""MATCH (chapter:ChapterNode {{chapter_name: "{chapter_name}"}}),
            """
            
            # 匹配所有子章节节点
            for i, subchapter in enumerate(subchapters):
                query += f"      (s{i}:SubChapterNode {{subchapter_name: \"{subchapter.replace('_', ' ')}\"}}){',' if i < len(subchapters) - 1 else ''}\n"
            
            query += "CREATE "
            
            # 创建从章节到子章节的关系
            for i, subchapter in enumerate(subchapters):
                query += f"(chapter)-[:HAS_SUBCHAPTER]->(s{i}){',' if i < len(subchapters) - 1 else ''}\n"
            
            query += ";"
            statements.append(query)
    
    return statements

# 生成子章节与概念之间关系的Cypher语句
def generate_subchapter_concept_relationships(data):
    statements = []
    
    for chapter_name, chapter_data in data.items():
        for subchapter_name, subchapter_data in chapter_data.items():
            if isinstance(subchapter_data, dict) and "描述" in subchapter_data:
                # 找出该子章节的所有概念
                concepts = []
                for concept_name, concept_data in subchapter_data.items():
                    if isinstance(concept_data, dict) and "描述" in concept_data:
                        safe_concept_name = f"{subchapter_name}_{concept_name}".replace(" ", "_")
                        concepts.append(safe_concept_name)
                
                if concepts:
                    # 创建关系查询
                    safe_subchapter_name = subchapter_name.replace(" ", "_")
                    query = f"""MATCH (subchapter:SubChapterNode {{subchapter_name: "{subchapter_name}"}}),
                    """
                    
                    # 匹配所有概念节点
                    for i, concept in enumerate(concepts):
                        original_concept_name = concept.replace(f"{subchapter_name}_", "").replace("_", " ")
                        query += f"      (c{i}:ConceptNode {{concept_name: \"{original_concept_name}\"}}){',' if i < len(concepts) - 1 else ''}\n"
                    
                    query += "CREATE "
                    
                    # 创建从子章节到概念的关系
                    for i, concept in enumerate(concepts):
                        query += f"(subchapter)-[:HAS_CONCEPT]->(c{i}){',' if i < len(concepts) - 1 else ''}\n"
                    
                    query += ";"
                    statements.append(query)
    
    return statements

# 主函数：处理JSON并生成Neo4j数据库
def create_knowledge_graph(json_data, driver):
    try:
        # 解析JSON数据
        data = json.loads(json_data) if isinstance(json_data, str) else json_data
        
        # 清空数据库（可选）
        clean_database(driver)
        
        # 生成并执行Cypher语句
        all_statements = []
        all_statements.extend(generate_chapter_nodes(data))  # 生成章节节点
        all_statements.extend(generate_subchapter_nodes(data))  # 生成子章节节点
        all_statements.extend(generate_concept_nodes(data))  # 生成概念节点
        all_statements.extend(generate_chapter_subchapter_relationships(data))  # 生成章节与子章节的关系
        all_statements.extend(generate_subchapter_concept_relationships(data))  # 生成子章节与概念的关系
    
        # 执行所有Cypher语句
        for statement in all_statements:
            print(f"正在执行: {statement[:100]}...")  # 打印前100个字符用于调试
            run_cypher_query(driver, statement)
        
        print(f"知识图谱创建成功，共执行了{len(all_statements)}条Cypher语句")
        
    except Exception as e:
        print(f"创建知识图谱失败: {e}")

# 主程序执行
if __name__ == "__main__":
    # 从文件加载JSON数据
    with open("new_format.json", "r", encoding="utf-8") as f:
        json_data = f.read()
    
    # 连接到Neo4j
    driver = connect_to_neo4j()
    
    if driver:
        # 创建知识图谱
        create_knowledge_graph(json_data, driver)
        
        # 关闭Neo4j连接
        close_neo4j_connection(driver)
