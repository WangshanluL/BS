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

请注意，在你添加引用来源时宁缺毋滥，不要随意添加引用标签,当且仅当回答中某句话用到了某页互联网信息时才在这句话后面添加
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
请注意，在你添加引用来源时宁缺毋滥，不要随意添加引用标签,当且仅当回答中某句话用到了某页互联网信息时才在这句话后面添加
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
def format_video_links(answer, relevant_video_links):
    """
    将相关视频链接格式化并添加到回答后面（纯文本格式）

    参数:
    answer (str): 知识图谱问答的回答
    relevant_video_links (list): 包含视频信息的字典列表，每个字典有video_title和video_url键

    返回:
    str: 添加了相关视频链接的完整回答
    """
    # 如果没有相关视频，直接返回原始回答
    if not relevant_video_links:
        return answer

    # 添加相关视频部分
    formatted_answer = answer.strip()

    # 添加分隔线和相关视频标题（带电视符号）
    formatted_answer += "\n\n📺 相关学习视频推荐：\n\n"

    # 添加视频链接
    for i, video in enumerate(relevant_video_links, 1):
        title = video.get("video_title", "未知标题")
        url = video.get("video_url", "#")
        formatted_answer += f"{i}. {title}\n   {url}\n\n"

    return formatted_answer
def get_last_three_conversation_pairs(history_messages):
    """
    从对话历史中获取最后三组完整的user-assistant对话对

    参数:
    history_messages: 包含所有历史消息的列表

    返回:
    list: 包含最后三组完整对话的消息列表
    """
    messages = []
    conversation_pairs = []

    # 反向遍历所有消息，找出完整的对话对
    i = len(history_messages) - 1
    while i >= 0 and len(conversation_pairs) < 3:
        # 查找assistant消息
        assistant_message = None
        while i >= 0 and assistant_message is None:
            if history_messages[i].role == "assistant":
                assistant_message = history_messages[i]
            i -= 1

        # 查找对应的user消息
        user_message = None
        while i >= 0 and user_message is None:
            if history_messages[i].role == "user":
                user_message = history_messages[i]
            i -= 1

        # 如果找到了一组完整的对话，添加到结果中
        if user_message is not None and assistant_message is not None:
            conversation_pairs.append((user_message, assistant_message))

    # 反转顺序，使最早的对话在前
    conversation_pairs.reverse()

    # 添加到最终消息列表
    for user_msg, assistant_msg in conversation_pairs:
        messages.append({"role": user_msg.role, "content": user_msg.content})
        messages.append({"role": assistant_msg.role, "content": assistant_msg.content})

    return messages