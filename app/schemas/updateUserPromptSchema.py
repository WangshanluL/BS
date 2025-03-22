def get_os_qa_prompt(search_options=None, question="", internet_info="", knowledge_graph=""):
    """
    根据搜索选项获取相应的操作系统问答系统提示词模板，并填充检索信息。

    参数:
    search_options (dict): 包含搜索选项的字典，格式为 {"knowledgeGraph": 0/1, "internet": 0/1}
    question (str): 用户的问题
    internet_info (str): 从互联网检索的信息
    knowledge_graph (str): 从知识图谱检索的信息

    返回:
    str: 填充好的提示词模板
    """

    # 定义引用格式提示
    citation_instruction = """
## 引用格式说明
在使用互联网检索信息时，请以[citation:n]格式标注引用来源，其中n表示引用的网页编号。
例如：
- "Linux内核是一个单内核设计[citation:1]" 表示这句话引用了网页1的内容
- "Windows采用混合内核架构[citation:2]" 表示这句话引用了网页2的内容

请确保所有来自互联网的信息都有适当的引用标注。
"""

    # 定义四种搜索选项组合的提示词模板 (00, 01, 10, 11)
    os_qa_prompts = {
        # 0 0 - 什么都不需要
        "00": """# 
你是一个专门回答操作系统相关问题的AI助手。请提供准确、专业且有深度的回答。

## 专业知识领域
- 操作系统核心概念（进程管理、内存管理、文件系统等）
- 主流操作系统（Windows、Linux、macOS、Unix、Android、iOS）
- 系统架构、并发与同步、内存虚拟化、文件系统
- 系统调用、安全机制、网络协议栈
- 性能优化、问题排查与故障分析

## 回答指南
- 使用专业术语并提供清晰解释
- 根据问题复杂度调整回答深度
- 在适当情况下使用代码示例或配置示例

用户问题: {question}

请直接回答上述问题。""",

        # 0 1 - 只需要互联网信息
        "01": """# 
你是一个专门回答操作系统相关问题的AI助手。请提供准确、专业且有深度的回答。

## 专业知识领域
- 操作系统核心概念（进程管理、内存管理、文件系统等）
- 主流操作系统（Windows、Linux、macOS、Unix、Android、iOS）
- 系统架构、并发与同步、内存虚拟化、文件系统
- 系统调用、安全机制、网络协议栈
- 性能优化、问题排查与故障分析

## 互联网检索信息
以下是从互联网获取的相关信息:
{internet_info}

{citation_instruction}

用户问题: {question}

请利用上述互联网检索的信息回答问题，保持专业性和准确性，并使用[citation:n]格式标注引用来源。""",

        # 1 0 - 仅知识图谱信息
        "10": """# 
你是一个专门回答操作系统相关问题的AI助手。请提供准确、专业且有深度的回答。

## 知识图谱查询结果
以下是你从操作系统知识图谱查询返回的知识信息:
{knowledge_graph}

用户问题: {question}

请综合利用知识图谱查询结果来回答用户问题，确保回答的专业性和准确性。在回答中可以引用具体的知识图谱查询结果。""",

        # 1 1 - 互联网 + 知识图谱
        "11": """# 
你是一个专门回答操作系统相关问题的AI助手。请提供准确、专业且有深度的回答。

## 互联网检索信息
以下是从互联网获取的相关信息:
{internet_info}

## 知识图谱查询结果
以下是知识图谱查询返回的相关结果:
{knowledge_graph}

{citation_instruction}

用户问题: {question}

请综合利用互联网信息和知识图谱查询结果回答用户问题。确保回答的专业性和准确性，并在适当的地方引用知识图谱结果。使用[citation:n]格式标注引用互联网信息的来源。"""
    }

    # 如果没有传入搜索选项，默认全部为0
    if search_options is None:
        search_options = {"knowledgeGraph": 0, "internet": 0}

    # 获取各个选项的值
    kg = search_options.get("knowledgeGraph", 0)
    internet = search_options.get("internet", 0)

    # 生成选项键
    option_key = f"{kg}{internet}"

    # 获取对应的提示词模板
    prompt_template = os_qa_prompts.get(option_key, os_qa_prompts["00"])  # 默认使用 "00"

    # 填充实际数据，对于internet=1的情况需要插入引用格式说明
    citation_text = citation_instruction if internet == 1 else ""

    final_prompt = prompt_template.format(
        question=question,
        internet_info=internet_info,
        knowledge_graph=knowledge_graph,
        citation_instruction=citation_text
    )

    return final_prompt