import os 
import json
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
import ast

# 设置API环境变量
os.environ["OPENAI_API_KEY"] = "sk-QKpXTlx9lWqDX5mdC1F1FaAcF5F34c1b9bBe9244D96a53F7"
os.environ["OPENAI_API_BASE"] = "https://api.xty.app/v1"

# 知识点节点列表
knowledge_nodes = ['存储设备-寄存器, 高速缓存, 内存, 磁盘缓存, 固定磁盘, 可移动存储介质', '编译方式-编译, 链接, 装入', '链接方式-静态链接, 装入时动态链接, 运行时动态链接', '装入方式-绝对装入, 可重定位装入, 动态运行时装入', '连续分配-单一连续分配, 固定分区分配, 动态分区分配, 动态重定位分区分配', '分配策略-首次适 应算法(空闲分区地址递增), 循环首次适应算法(循环查找), 最佳适应算法(空闲分区容量递增), 最坏适应算法(空闲分区容量递减)', '离散分配-分页存储管理(有内碎片),  分段存储管理(有外碎片), 段页式存储管理(有内碎片)', '文件定义-具有文件名的一组相关信息的集合', '文件分类-系统文件, 用户文件, 库文件, 只执行文件, 只读文件, 读/写文件, 普通文件, 目录文件, 特殊文件, 源文件, 目标文件, 可执行文件', '层次结构-最高层(文件系统接口), 中间层(对象管理软件), 最底层(存储对象及其属性)', '逻辑结构-无结构文件(流式文件), 顺序文件(存取速度快, 但插入删除困难), 索引文件(检索速度快, 但系统开销大), 索引顺序文件(支持顺序和随机访问)', '目录组织-单级目录, 两级目录, 树形目录, 无环图目录', '索引机制-FCB(文件控制块), 索引节点', '共享方式-索引节点共享, 符号链接共享', '访问控制-访问权和保护域, 访问矩阵', '局部性原理-时间局部性, 空间局部性', '特性-多次性, 对换性, 虚拟性', '分页机制-页表机制, 缺页中断机构, 地址变换机构', '置换算法-最佳置换算法, FIFO, LRU, LFU, Clock', '页面分配-预调页策略, 请求调页策略', '性能问题-抖动, 工作集', '进程定义-进程是程序的运行过程, 是资源分配和调度的基本单位', '进程状态-就绪(等待CPU), 执行(正在运行), 阻塞(等待事件发生)', '进程控制-创建, 终止, 阻塞, 唤醒, 挂起, 激活', '进程组成-PCB(进程控制块), 程序段, 数据段', '进程通信-共享存储, 消息传递, 管道通信', '线程定义-线程是进程内的执行单元, 是处理器调度的基本单位', '实现方式-内核线程(由操作系统管理), 用户级线程(由应用程序管理)', '模式-内核 态, 用户态', '中断与异常-外中断, 内中断', '系统调用-用户程序与操作系统交互的接口', '基本特性-并发(多个事件同时发生), 共享(资源共享), 虚拟(物理资源虚拟化), 异步(进程以不可预测的速度执行)', '核心功能-进程管理(进程控制, 同步, 通信, 调度), 存储管理(内存分配, 保护, 映射, 扩充), 设备管理(缓冲管理, 设备分配, 设备 控制), 文件管理(存储管理, 目录管理, 读写管理, 保护)', '阶段-无操作系统, 单道批处理, 多道批处理, 分时系统, 实时系统, 微机操作系统', '架构类型-模块化, 分层 式, 微内核', 'IO设备-分类方式：按使用特性分为输入设备（键盘、鼠标)、输出设备（打印机、绘图仪)、交互设备（显示器)；按传输速率分为低速设备（键盘、鼠标)、中 速设备（激光打印机)、高速设备（磁带机、磁盘机)', '功能-控制IO设备,实现设备与计算机的数据交换', '设备控制器-组成部分：与处理机的接口,与设备的接口', '通道- 建立独立的IO操作,可能存在瓶颈问题', '轮询IO-过程简单,CPU利用率低', '中断IO-以字节为单位进行IO,提高CPU利用率', 'DMA-直接在IO设备和内存之间传输数据,以数据块为单位', '通道控制-通道程序控制IO设备进行数据传输,一次可传输一组数据块', '设备无关软件-设备独立性：逻辑设备名与物理设备名分离；设备分配考虑因素：设备属性 、分配算法、安全性', 'SPOOLing系统-包含IO井、IO缓冲区、IO进程、井管理程序,特点：提高IO速度,实现虚拟设备功能', '连续组织-优点：顺序访问速度快；缺点：要求空间连续,需提前确定文件大小,动态增长困难', '链接组织-优点：外存利用率高,支持动态增长；缺点：不支持高效直接存取。隐式链接：每个盘块存储下一个盘块的位置指针, 可靠性差。显式链接：物理块信息存储于FAT表,检索速度快,但占用内存空间', '索引组织-优点：支持直接访问,查找速度快,外存利用率高；缺点：索引块占用磁盘空间,索引 块利用率低,索引级数增加导致磁盘访问次数增加。索引方式：单级索引、多级索引、增量式索引', '空闲区表法-连续分配方式,建立空闲表,每个空闲区对应一个表项', '空闲链表法-所有空闲盘区连成一条空闲链', '位示图法-用二进制位表示磁盘盘块的使用情况', '成组链接法-UNIX/Linux文件系统采用的管理方法,将空闲块分组链接', '磁盘缓存-提高磁盘IO效率的缓存机制', '优化方法-提前读,延迟写,优化物理块分布,虚拟盘', 'RAID-廉价磁盘冗余阵列', '容错技术-第一级容错,第二级容错', '后备系统-备用系统 确保数据的可靠性', '集群容错-基于集群系统的容错技术', '资源利用率-最大化系统中处理机和资源的使用', '系统吞吐量-单位时间内完成的作业数', '公平性-防止进程饥饿,合理分配CPU时间', '响应时间-尽可能缩短', '周转时间-尽可能缩短周转时间和带权周转时间', '高级调度-作业调度', '中级调度-内存调度', '低级调度-进程调度', ' 非抢占调度-进程执行完毕前不会被抢占', '抢占调度-调度策略包括优先级、短进程优先、时间片', '先来先服务-按照作业到达的先后顺序调度', '短作业优先-作业越短,优 先级越高', '优先级调度-基于紧迫性赋予不同优先级', '高响应比优先-响应比计算公式：(等待时间 + 要求服务时间) / 要求服务时间', '轮转调度-每个进程每次运行一个 时间片', '多级反馈队列-划分多个就绪队列,优先级不同', '死锁原因-竞争资源,进程推进顺序非法', '死锁必要条件-互斥、请求保持、不可抢占、循环等待', '死锁处理-预防死锁（破坏必要条件),避免死锁（银行家算法),检测死锁（分析资源请求和分配),解除死锁（抢占资源或终止进程)', '临界资源-一次仅供一个进程使用的资源', '临界区- 访问临界资源的代码段', '同步准则-空闲让进、忙则等待、有限等待、让权等待', '软件机制-Peterson算法、关中断', '硬件机制-Test-and-Set指令、Swap指令、信号量机 制（整型信号量、记录型信号量、AND型信号量、信号量集)', '管程-提供同步进程和数据操作的方法', '生产者消费者-多个生产者和消费者通过缓冲区共享数据', '哲学家进餐-避免死锁和饥饿的资源分配问题', '读者写者-控制多个读者和写者对共享资源的访问']
def split_text_into_chunks(text, chunk_size=750, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

def setup_parser():
    response_schemas = [
        ResponseSchema(name="topic_name", description="题目主要考察内容"),
        ResponseSchema(name="topic_type", description="题目类型，填空题为1，选择题为2"),
        ResponseSchema(name="topic_description", description="题目描述"),
        ResponseSchema(name="topic_answer", description="标准答案"),
        ResponseSchema(name="topic_answer_reason", description="答案解析，200-500字"),
        ResponseSchema(name="topic_word", description="相关知识点列表")
    ]
    return StructuredOutputParser.from_response_schemas(response_schemas)

def process_text_document(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    text_chunks = split_text_into_chunks(text)
    knowledge_nodes_str = "、".join(knowledge_nodes)
    
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7, max_tokens=1500)
    parser = setup_parser()
    format_instructions = parser.get_format_instructions()
    
    system_message = SystemMessage(content="您是一名专业的操作系统试卷分析专家，擅长提供深入、专业的技术解析。")
    user_template = """
    您是一名精通操作系统的专业教师和试卷分析专家。请仔细分析以下题目：
你最关键的任务是从下面只能用知识点节点中选择与题目相关的知识点节点，相当于为题目打标签topic_word，但标签只能是下面只能用的知识点节点,
请注意，知识点节点有详细的描述，请你根据描述选择比较相关的知识点节点，不需要输出描述
为了方面你理解如何把题目精准匹配知识点节点，我为每个知识点节点都加入了描述，比如生产者消费者-多个生产者和消费者通过缓冲区共享数据，-后面的是描述
你只需要在理解的时候使用，输出topic_word的时候不要输出-后面的东西
只能用的知识点节点：{}         

题目内容：{}

您需要完成以下任务：
1. 从提供的知识点节点中，准确识别与题目相关的知识点 （topic_word）,请你记住，只能选择我给出的可用的知识点节点，选一个最相关的
2. 判断题目类型（填空题为1，选择题为2）
3. 给出标准答案
4. 详细撰写答案解析（topic_answer_reason）
5. 请你务必关注下面题目的topic_word只能是上面给出的知识点节点里的词。
6.若题目不完整，可以忽略此题目


重点要求：
- **输出格式**：必须是一个列表，每个列表元素为一个字典，且包含以下字段：
  - `topic_name`：题目主要考察内容
  - `topic_type`：题目类型，填空题为1，选择题为2
  - `topic_description`：题目描述,这里一定要详细记录原来题目的描述，包括题目的选项,后续会取出节点,若题目描述不完整，可不输出此题目
  - `topic_answer`：标准答案
  - `topic_answer_reason`：答案解析（200-500字）
  - `topic_word`：相关知识点列表，请你务必重视，这个知识点列表只能是上面给出的知识点列表里的词，我需要题目与上面知识点节点关联起来，务必重视。
  

- **答案解析（topic_answer_reason）**：
  - 提供深入、专业的知识背景解释
  - 详细阐述答案的理论依据
  - 解释为什么选择这个答案
  - 如果是概念性问题，解释概念的本质和重要性
  - 如果是技术性问题，详细说明技术原理和应用场景
  - 使用清晰、学术性的语言
  - 篇幅在200-500字之间
  - 可以适当引用操作系统领域的经典理论或案例

请确保答案解析专业、详细，体现对操作系统知识的深入理解。
注意，输出必须是完整的一个列表，列表下是一个个完整的字典。不需要输出其他内容.
注意，输出必须是完整的一个列表，列表下是一个个完整的字典。不需要输出其他内容.
注意，输出必须是完整的一个列表，列表下是一个个完整的字典。不需要输出其他内容.
**输出示例**：
[
    {{
        "topic_name": "进程管理",
        "topic_type": 2,
        "topic_description": "以下关于进程状态的说法中，哪个是正确的？A.进程 B.线程 C.进程和线程 D.只有进程",
        "topic_answer": "B",
        "topic_answer_reason": "进程的状态包括就绪、运行和等待状态......（详细解析 200-500 字）",
        "topic_word": ["进程状态", "调度算法"]
    }}
]

    """
    correct_file = "First_abstract_answers.txt"
    error_file = "Third_error_answers.txt"
    def save_to_file(filename, data):
        """将数据追加到指定文件"""
        with open(filename, "a", encoding="utf-8") as f:
            f.write(str(data) + "\n")  # 追加一行数据



    error_answer = []
    exam_questions = []
    for text_chunk in text_chunks:
        userprompt = user_template.format(knowledge_nodes_str,text_chunk)
        user_message = HumanMessage(content=userprompt)
        try:
            response = chat([system_message, user_message])
        #print(response.content)

            python_list = ast.literal_eval(response.content)
            exam_questions.append(python_list)
            save_to_file(correct_file,python_list)
            print(f"处理完成{python_list}")
        except Exception as e:
            print(f"处理题目时出错: {e}")
            error_answer.append(response.content)
            save_to_file(error_file,text_chunk)


    
    return exam_questions

file_path = 'Second_error_answers.txt'
result = process_text_document(file_path)

if result:
    print(json.dumps(result, ensure_ascii=False, indent=2))
else:
    print("未处理任何题目")
