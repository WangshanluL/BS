import asyncio
from app.utils.RagFromNeo4j import ragFromNeo4j
from app.utils.RagFromTavily import search_tavily
from app.schemas.updateUserPromptSchema import get_os_qa_prompt

async def rag_and_update_prompt(prompt: str, search_options: dict):
    """
    根据搜索选项决定是否进行知识图谱查询和互联网检索，并返回相应结果

    参数:
    prompt (str): 用户的查询提示
    search_options (dict): 搜索选项字典，包含knowledgeGraph、internet和learningMaterials的配置

    返回:
    tuple: (LLM_PROMPT, relevant_nodes_links, tavily_results) 包含提示词、知识图谱结果和互联网检索结果
    """
    # 从搜索选项中获取各项设置
    knowledge_graph_enabled = search_options.get("knowledgeGraph", 0) == 1
    learning_materials_enabled = search_options.get("learningMaterials", 0) == 1
    internet_enabled = search_options.get("internet", 0) == 1

    # 初始化结果变量
    tavily_results = {"results": [],"contents":""}
    neo4j_str_corpus = ""
    relevant_nodes_links = []
    tasks = []

    # 如果internet为1，则调用互联网检索
    if internet_enabled:
        tavily_task = asyncio.create_task(search_tavily(prompt))
        tasks.append(tavily_task)
    # 如果knowledgeGraph或learningMaterials有一个为1，则调用知识图谱查询
    if knowledge_graph_enabled or learning_materials_enabled:
        neo4j_task = asyncio.create_task(ragFromNeo4j(prompt))
        tasks.append(neo4j_task)



    # 如果有任务需要执行，则等待完成
    if tasks:
        results = await asyncio.gather(*tasks)

        # 解析结果
        result_index = 0

        # 如果执行了互联网检索任务，获取其结果
        if internet_enabled:
            res= results[result_index]
            tavily_results["results"],tavily_results["contents"] = res
            result_index += 1

        # 如果执行了知识图谱查询任务，获取其结果
        if knowledge_graph_enabled or learning_materials_enabled:
            neo4j_results = results[result_index]
            neo4j_str_corpus, relevant_nodes_links = neo4j_results
    LLM_PROMPT = get_os_qa_prompt(search_options,prompt,tavily_results.get("contents",""),neo4j_str_corpus)
    # 保持原始提示词

    return LLM_PROMPT, relevant_nodes_links, tavily_results.get("results", [])


