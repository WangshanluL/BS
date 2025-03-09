import json
from neo4j import GraphDatabase
import ast


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


# 获取当前题目计数
def get_topic_count(driver):
    query = """
    MATCH (topic:TopicNode)
    RETURN COUNT(topic) AS count
    """
    result = run_cypher_query(driver, query)
    if result:
        record = result.single()
        if record:
            return record["count"] + 1
    return 1


# 创建题目节点
def create_topic_node(driver, topic_data, topic_counter):
    try:
        # 从JSON中获取题目信息
        original_topic_name = topic_data.get("topic_name", "")
        # 添加题目编号前缀
        topic_name = f"题目{topic_counter}:{original_topic_name}"

        topic_type = topic_data.get("topic_type", 0)
        topic_description = topic_data.get("topic_description", "").replace('"', '\\"')  # 转义双引号
        topic_answer = topic_data.get("topic_answer", "").replace('"', '\\"')
        topic_answer_reason = topic_data.get("topic_answer_reason", "").replace('"', '\\"')

        # 为TopicNode创建一个唯一的ID（使用topic_name的安全版本）
        safe_topic_name = topic_name.replace(" ", "_").replace('"', '')

        # 创建题目节点的Cypher查询
        query = f"""
        CREATE (topic:TopicNode {{
            topic_name: "{topic_name}",
            topic_type: {topic_type},
            topic_description: "{topic_description}",
            topic_answer: "{topic_answer}",
            topic_answer_reason: "{topic_answer_reason}"
        }})
        RETURN topic
        """

        # 执行查询并获取结果
        result = run_cypher_query(driver, query)
        if result:
            print(f"成功创建题目节点: {topic_name}")
            return safe_topic_name, topic_name
        else:
            print(f"创建题目节点失败: {topic_name}")
            return None, topic_name

    except Exception as e:
        print(f"创建题目节点时出错: {e}")
        return None, topic_data.get("topic_name", "")


# 建立题目与概念之间的关系
def create_topic_concept_relationships(driver, safe_topic_name, topic_name, topic_words):
    try:
        if not topic_words:
            print(f"题目 {safe_topic_name} 没有关联的概念词")
            return

        for concept in topic_words:
            # 创建关系的Cypher查询
            # 使用完整的新名称（带前缀）来匹配题目节点
            query = f"""
            MATCH (concept:ConceptNode {{concept_name: "{concept}"}}),
                  (topic:TopicNode {{topic_name: "{topic_name}"}})
            CREATE (concept)-[:relation_topics]->(topic)
            """

            result = run_cypher_query(driver, query)
            if result:
                print(f"成功创建关系: 概念[{concept}] -> 题目[{topic_name}]")
            else:
                print(f"创建关系失败: 概念[{concept}] -> 题目[{topic_name}]")

                # 如果创建关系失败，可能是因为ConceptNode不存在，可以选择创建一个
                create_concept_query = f"""
                CREATE (concept:ConceptNode {{
                    concept_name: "{concept}",
                    description: "自动创建的概念节点"
                }})
                """

                # 执行创建概念节点的查询
                run_cypher_query(driver, create_concept_query)
                print(f"已创建新的概念节点: {concept}")

                # 再次尝试创建关系
                run_cypher_query(driver, query)
                print(f"重新尝试创建关系: 概念[{concept}] -> 题目[{topic_name}]")

    except Exception as e:
        print(f"创建题目与概念关系时出错: {e}")


# 处理单行数据（包含多个题目）
def process_line(driver, line, start_counter):
    try:
        # 解析JSON数据
        topics = ast.literal_eval(line)
        counter = start_counter

        # 处理每个题目
        for topic_data in topics:
            # 创建题目节点
            safe_topic_name, topic_name = create_topic_node(driver, topic_data, counter)
            counter += 1

            if safe_topic_name:
                # 获取题目关联的概念词列表
                topic_words = topic_data.get("topic_word", [])

                # 创建与概念的关系
                create_topic_concept_relationships(driver, safe_topic_name, topic_name, topic_words)

        return counter

    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return start_counter
    except Exception as e:
        print(f"处理数据行时出错: {e}")
        return start_counter


# 主函数：从文件读取数据并处理
def process_topic_file(file_path, driver):
    try:
        # 获取当前题目计数作为起始值
        topic_counter = 0
        print(f"开始处理，起始题目编号: {topic_counter}")

        with open(file_path, "r", encoding="utf-8") as f:
            line_count = 0
            for line in f:
                line = line.strip()
                if line:  # 确保行不为空
                    line_count += 1
                    print(f"正在处理第 {line_count} 行数据...")
                    topic_counter = process_line(driver, line, topic_counter)

        print(f"处理完成，共处理了 {line_count} 行数据")

    except Exception as e:
        print(f"处理文件时出错: {e}")


# 主程序执行
if __name__ == "__main__":
    # 文件路径
    file_path = "First_abstract_answers.txt"  # 请替换为你的文件路径

    # 连接到Neo4j
    driver = connect_to_neo4j()

    if driver:
        # 处理题目文件
        process_topic_file(file_path, driver)

        # 关闭Neo4j连接
        close_neo4j_connection(driver)