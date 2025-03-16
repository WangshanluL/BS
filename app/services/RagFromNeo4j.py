import asyncio  # 导入 asyncio 以运行异步函数
from app.utils.rerank_aliyun import RerankerCompressor
from app.core.log_config import logger
from typing import List
from app.db.db_neo4j import async_neo4j_driver
from typing import List, Dict, Any

import re
pattern = r'^(.*?)->'

# 读取文件内容
with open("../utils/output.txt", "r", encoding="utf-8") as file:
    lines = [line.strip() for line in file.readlines()]  # 去除换行符并存入列表

# 定义异步运行函数
async def rerank_and_extract_conceptNode(prompt:str,similarity_threshold:float = 0.48)->List[str]:
    res = await RerankerCompressor.base_text_rerank(
        lines, prompt , len(lines)
    )
    filter_res = []
    for rank in res:
        if rank["relevance_score"] >= similarity_threshold:
            filter_res.append(rank["document"]["text"])
        else:
            break
    extracted = [re.match(pattern, text).group(1) for text in filter_res if re.match(pattern, text)]
    logger.info(f"与prompt{prompt}比较相关的知识点节点为:{extracted}")
    return extracted



async def retrieve_knowledge_graph(concept_names_list: list[str]):
    """
    根据提供的概念名称列表从知识图谱中检索相关节点和关系，并构建节点和链接数组
    处理Neo4j返回的字典结果

    参数:
    concept_names_list: 概念名称的字符串列表

    返回:
    dict: 包含 nodes 和 links 的字典
    """
    # 初始化节点和链接数组
    nodes = []
    links = []
    node_id_map = {}  # 用于存储节点映射，使用Neo4j返回的节点识别方式
    next_id = 0

    try:
        # 1. 查询匹配的ConceptNode节点
        async def get_concept_nodes(concept_names_list):
            concept_names_param = ', '.join([f'"{name}"' for name in concept_names_list])
            query = f"""
            MATCH (concept:ConceptNode)
            WHERE concept.concept_name IN [{concept_names_param}]
            RETURN concept
            """
            async with async_neo4j_driver.session() as session:
                result = await session.run(query)
                return await result.data()

        # 2. 查询所有ConceptNode的父节点(SubChapterNode)
        async def get_parent_nodes(concept_names_list):
            concept_names_param = ', '.join([f'"{name}"' for name in concept_names_list])
            query = f"""
            MATCH (concept:ConceptNode)
            WHERE concept.concept_name IN [{concept_names_param}]
            MATCH (parent:SubChapterNode)-[r:HAS_CONCEPT]->(concept)
            RETURN parent, concept
            """
            async with async_neo4j_driver.session() as session:
                result = await session.run(query)
                return await result.data()

        # 3. 查询父节点下的所有ConceptNode(同级概念)
        async def get_sibling_concepts(concept_names_list):
            concept_names_param = ', '.join([f'"{name}"' for name in concept_names_list])
            query = f"""
            MATCH (concept:ConceptNode)
            WHERE concept.concept_name IN [{concept_names_param}]
            MATCH (parent:SubChapterNode)-[:HAS_CONCEPT]->(concept)
            MATCH (parent)-[r:HAS_CONCEPT]->(sibling:ConceptNode)
            RETURN sibling, parent
            """
            async with async_neo4j_driver.session() as session:
                result = await session.run(query)
                return await result.data()

        # 4. 查询所有ConceptNode的TopicNode
        async def get_topic_nodes(concept_names_list):
            concept_names_param = ', '.join([f'"{name}"' for name in concept_names_list])
            query = f"""
            MATCH (concept:ConceptNode)
            WHERE concept.concept_name IN [{concept_names_param}]
            MATCH (concept)-[r:HAS_TOPIC]->(topic:TopicNode)
            RETURN topic, concept
            """
            async with async_neo4j_driver.session() as session:
                result = await session.run(query)
                return await result.data()

        # 5. 查询所有ConceptNode的VideoNode
        async def get_video_nodes(concept_names_list):
            concept_names_param = ', '.join([f'"{name}"' for name in concept_names_list])
            query = f"""
            MATCH (concept:ConceptNode)
            WHERE concept.concept_name IN [{concept_names_param}]
            MATCH (concept)-[r:HAS_VIDEO]->(video:VideoNode)
            RETURN video, concept
            """
            async with async_neo4j_driver.session() as session:
                result = await session.run(query)
                return await result.data()

        # 生成节点唯一标识符
        def get_node_key(node_dict, label):
            # 使用节点的主要属性作为唯一标识符
            if label == 'ConceptNode':
                return f"concept_{node_dict['concept_name']}"
            elif label == 'SubChapterNode':
                return f"subchapter_{node_dict['subchapter_name']}"
            elif label == 'TopicNode':
                return f"topic_{node_dict['topic_name']}"
            elif label == 'VideoNode':
                return f"video_{node_dict['video_name']}"
            else:
                # 如果无法确定标签，使用所有属性值组合
                return str(hash(frozenset(node_dict.items())))

        # 并行执行所有查询
        tasks = [
            get_concept_nodes(concept_names_list),
            get_parent_nodes(concept_names_list),
            get_sibling_concepts(concept_names_list),
            get_topic_nodes(concept_names_list),
            get_video_nodes(concept_names_list)
        ]

        results = await asyncio.gather(*tasks)
        concept_records = results[0]
        parent_records = results[1]
        sibling_records = results[2]
        topic_records = results[3]
        video_records = results[4]

        # 处理概念节点
        for record in concept_records:
            concept = record['concept']

            # 生成唯一标识符
            concept_key = get_node_key(concept, 'ConceptNode')

            if concept_key not in node_id_map:
                node_id_map[concept_key] = next_id
                nodes.append({
                    'id': next_id,
                    'name': concept.get('concept_name', 'Unknown'),
                    'category': 3,  # ConceptNode
                    'value': concept.get('description', '')
                })
                next_id += 1

        # 处理父节点和概念节点的关系
        for record in parent_records:
            parent = record['parent']
            concept = record['concept']

            # 生成唯一标识符
            concept_key = get_node_key(concept, 'ConceptNode')
            parent_key = get_node_key(parent, 'SubChapterNode')

            # 确保概念节点已添加
            if concept_key not in node_id_map:
                node_id_map[concept_key] = next_id
                nodes.append({
                    'id': next_id,
                    'name': concept.get('concept_name', 'Unknown'),
                    'category': 3,  # ConceptNode
                    'value': concept.get('description', '')
                })
                next_id += 1

            # 添加父节点
            if parent_key not in node_id_map:
                node_id_map[parent_key] = next_id
                nodes.append({
                    'id': next_id,
                    'name': parent.get('subchapter_name', 'Unknown'),
                    'category': 2,  # SubChapterNode
                    'value': parent.get('description', '')
                })
                next_id += 1

            # 添加父节点到概念的链接
            links.append({
                'source': node_id_map[parent_key],
                'target': node_id_map[concept_key],
                'type': 'HAS_CONCEPT'
            })

        # 处理同级概念节点
        for record in sibling_records:
            sibling = record['sibling']
            parent = record['parent']

            # 生成唯一标识符
            sibling_key = get_node_key(sibling, 'ConceptNode')
            parent_key = get_node_key(parent, 'SubChapterNode')

            # 添加父节点
            if parent_key not in node_id_map:
                node_id_map[parent_key] = next_id
                nodes.append({
                    'id': next_id,
                    'name': parent.get('subchapter_name', 'Unknown'),
                    'category': 2,  # SubChapterNode
                    'value': parent.get('description', '')
                })
                next_id += 1

            # 添加同级概念节点
            if sibling_key not in node_id_map:
                node_id_map[sibling_key] = next_id
                nodes.append({
                    'id': next_id,
                    'name': sibling.get('concept_name', 'Unknown'),
                    'category': 3,  # ConceptNode
                    'value': sibling.get('description', '')
                })
                next_id += 1

            # 添加父节点到同级概念的链接 (避免重复链接)
            parent_id = node_id_map[parent_key]
            sibling_id = node_id_map[sibling_key]

            link_exists = False
            for link in links:
                if (link['source'] == parent_id and
                        link['target'] == sibling_id and
                        link['type'] == 'HAS_CONCEPT'):
                    link_exists = True
                    break

            if not link_exists:
                links.append({
                    'source': parent_id,
                    'target': sibling_id,
                    'type': 'HAS_CONCEPT'
                })

        # 处理主题节点
        for record in topic_records:
            topic = record['topic']
            concept = record['concept']

            # 生成唯一标识符
            topic_key = get_node_key(topic, 'TopicNode')
            concept_key = get_node_key(concept, 'ConceptNode')

            # 确保概念节点已添加
            if concept_key not in node_id_map:
                node_id_map[concept_key] = next_id
                nodes.append({
                    'id': next_id,
                    'name': concept.get('concept_name', 'Unknown'),
                    'category': 3,  # ConceptNode
                    'value': concept.get('description', '')
                })
                next_id += 1

            # 添加主题节点
            if topic_key not in node_id_map:
                node_id_map[topic_key] = next_id
                nodes.append({
                    'id': next_id,
                    'name': topic.get('topic_name', 'Unknown'),
                    'category': 4,  # TopicNode
                    'value': topic.get('description', '')
                })
                next_id += 1

            # 添加概念到主题的链接
            links.append({
                'source': node_id_map[concept_key],
                'target': node_id_map[topic_key],
                'type': 'HAS_TOPIC'
            })

        # 处理视频节点
        for record in video_records:
            video = record['video']
            concept = record['concept']

            # 生成唯一标识符
            video_key = get_node_key(video, 'VideoNode')
            concept_key = get_node_key(concept, 'ConceptNode')

            # 确保概念节点已添加
            if concept_key not in node_id_map:
                node_id_map[concept_key] = next_id
                nodes.append({
                    'id': next_id,
                    'name': concept.get('concept_name', 'Unknown'),
                    'category': 3,  # ConceptNode
                    'value': concept.get('description', '')
                })
                next_id += 1

            # 添加视频节点
            if video_key not in node_id_map:
                node_id_map[video_key] = next_id
                nodes.append({
                    'id': next_id,
                    'name': video.get('video_name', 'Unknown'),
                    'category': 5,  # VideoNode
                    'value': video.get('description', '')
                })
                next_id += 1

            # 添加概念到视频的链接
            links.append({
                'source': node_id_map[concept_key],
                'target': node_id_map[video_key],
                'type': 'HAS_VIDEO'
            })

    except Exception as e:
        logger.error(f"知识图谱检索失败: {str(e)}")
        raise e

    return {
        'nodes': nodes,
        'links': links
    }
#再写两个函数，就是根据这个选择出相关词，然后两步筛选节点，然后修改格式，然后构成语料输出   `
# 运行异步函数
if __name__ == "__main__":
    #asyncio.run(rerank_and_extract_conceptNode("为什么操作系统要区分内核态和用户态？什么情况下需要切换？"))  # 正确执行异步函数
    asyncio.run(retrieve_knowledge_graph(['模式', '实现方式', '系统调用']))