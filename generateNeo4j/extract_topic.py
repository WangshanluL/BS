import os
import json
import openai
from langchain.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 设置OpenAI API
openai.api_key = 'sk-AQvWut1LZiaHbVBv885eC3D7FcBa441e9e4b52B5C265A4Cf'  # 请替换为您的API key
openai.api_base = 'https://api.xty.app/v1'  # 请替换为您的API base地址

# 知识点节点列表
knowledge_nodes = ['存储设备', '编译方式', '链接方式', '装入方式', '连续分配', '分配策略', '离散分配', '文件定义', '文件分类', '层次结构', '逻辑结构', '目录组 织', '索引机制', '共享方式', '访问控制', '局部性原理', '特性', '分页机制', '置换算法', '页面分配', '性能问题', '进程定义', '进程状态', '进程控制', '进程组成', '进程通信', '线程定义', '实现方式', '模式', '中断与异常', '系统调用', '基本特性', '核心功能', '阶段', '架构类型', 'IO设备', '功能', '设备控制器', '通道', '轮询IO', '中断IO', 'DMA', '通道控制', '设备无关软件', 'SPOOLing系统', '连续组织', '链接组织', '索引组织', '空闲区表法', '空闲链表法', '位示图法', ' 成组链接法', '磁盘缓存', '优化方法', 'RAID', '容错技术', '后备系统', '集群容错', '资源利用率', '系统吞吐量', '公平性', '响应时间', '周转时间', '高级调度', '中级调度', '低级调度', '非抢占调度', '抢占调度', '先来先服务', '短作业优先', '优先级调度', '高响应比优先', '轮转调度', '多级反馈队列', '死锁原因', '死锁必要条件', '死锁处理', '临界资源', '临界区', '同步准则', '软件机制', '硬件机制', '管程', '生产者消费者', '哲学家进餐', '读者写者']  # 您提供的完整列表

def process_word_document(file_path):
    # 加载Word文档
    loader = Docx2txtLoader(file_path)
    documents = loader.load()
    
    # 分割文档为页面
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=100
    )
    texts = text_splitter.split_documents(documents)
    
    # 将知识点节点转换为字符串
    knowledge_nodes_str = "、".join(knowledge_nodes)
    
    # 题目分析的Prompt模板
    prompt_template = f"""
    您是一名精通操作系统的专业教师和试卷分析专家。请仔细分析以下题目：

    可用知识点节点：{knowledge_nodes_str},请注意，知识点节点有详细的描述，请你根据描述选择比较相关的知识点节点，不需要输出描述.

    题目内容：{{question}}

    您需要完成以下任务：
    1. 从提供的知识点节点中，准确识别与题目相关的知识点
    2. 判断题目类型（填空题为1，选择题为2）
    3. 给出标准答案

    重点要求：对于答案解析(topic_answer_reason)，请遵循以下指导：
    - 提供深入、专业的知识背景解释
    - 详细阐述答案的理论依据
    - 解释为什么选择这个答案
    - 如果是概念性问题，解释概念的本质和重要性
    - 如果是技术性问题，详细说明技术原理和应用场景
    - 使用清晰、学术性的语言
    - 篇幅在200-500字之间
    - 可以适当引用操作系统领域的经典理论或案例

    返回JSON格式：
    {{
        "topic_name": "题目主要考察内容的概括",
        "topic_type": "题目类型（1或2）",
        "topic_description": "题目的详细描述",
        "topic_answer": "标准答案",
        "topic_answer_reason": "详细的、专业的答案解析，包括理论依据、概念阐释、应用场景等",
        "topic_word": ["相关知识点1", "相关知识点2", ...]
    }}

    请确保答案解析专业、详细，体现深入的操作系统知识理解。
    """

    exam_questions = []

    # 处理每个页面的文本
    for text in texts:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "您是一名专业的操作系统试卷分析专家，擅长提供深入、专业的技术解析。"},
                    {"role": "user", "content": prompt_template.format(question=text.page_content)}
                ],
                response_format={"type": "json_object"},
                max_tokens=1500,  # 增加Token数量以支持更详细的解析
                temperature=0.7
            )
            
            # 解析返回的JSON字符串
            question_analysis = json.loads(response.choices[0].message.content)
            exam_questions.append(question_analysis)
        
        except Exception as e:
            print(f"处理题目时出错: {e}")
    
    return exam_questions

# 使用示例
file_path = 'topics.docx'
result = process_word_document(file_path)
print(result) 