video_list = [
    {"title": "0.0 课程白嫖指南", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=1"},
    {"title": "1.1.1+1.1.3 操作系统的概念、功能", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=2"},
    {"title": "1.1.2 操作系统的特征", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=3"},
    {"title": "1.2_操作系统的发展与分类", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=4"},
    {"title": "1.3.1_操作系统的运行机制", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=5"},
    {"title": "1.3.2_中断和异常", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=6"},
    {"title": "1.3.3_系统调用", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=7"},
    {"title": "1.4_操作系统体系结构（上）", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=8"},
    {"title": "1.4_操作系统体系结构（下）", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=9"},
    {"title": "1.5_操作系统引导", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=10"},
    {"title": "1.6_虚拟机", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=11"},
    {"title": "2.1.1+2.1.2_进程的概念、组成、特征", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=12"},
    {"title": "2.1.3_进程的状态与转换", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=13"},
    {"title": "2.1.4_进程控制", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=14"},
    {"title": "2.1.5_进程通信", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=15"},
    {"title": "2.1.6_1 线程的概念与特点", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=16"},
    {"title": "2.1.6_2 线程的实现方式和多线程模型", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=17"},
    {"title": "2.1.6_3 线程的状态与转换", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=18"},
    {"title": "2.2.1 调度的概念、层次", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=19"},
    {"title": "2.2.2_1+2.2.4进程调度的时机、切换与过程、方式", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=20"},
    {"title": "2.2.2_2 调度器和闲逛进程", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=21"},
    {"title": "2.2.3 调度的目标（调度算法的评价指标）", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=22"},
    {"title": "2.2.5_1 调度算法：先来先服务、最短作业优先、最高响应比优先", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=23"},
    {"title": "2.2.5_2 调度算法：时间片轮转、优先级、多级反馈队列", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=24"},
    {"title": "2.2.5_3 调度算法：多级队列调度算法", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=25"},
    {"title": "2.3.1 同步与互斥的基本概念", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=26"},
    {"title": "2.3.2_1 进程互斥的软件实现方法", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=27"},
    {"title": "2.3.2_2 进程互斥的硬件实现方法", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=28"},
    {"title": "2.3.3_互斥锁", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=29"},
    {"title": "2.3.4_1 信号量机制", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=30"},
    {"title": "2.3.4_2 用信号量实现进程互斥、同步、前驱关系", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=31"},
    {"title": "2.3.5_1 生产者-消费者问题", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=32"},
    {"title": "2.3.5_2 多生产者-多消费者问题", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=33"},
    {"title": "2.3.5_3 吸烟者问题", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=34"},
    {"title": "2.3.5_4 读者-写者问题", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=35"},
    {"title": "2.3.5_5 哲学家进餐问题", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=36"},
    {"title": "2.3.6 管程", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=37"},
]



"""
您是一名专业教师。请你帮我完成下面任务，请你为我每个视频打上知识点标签，
但标签只能是下面只能用的知识点节点,
请注意，知识点节点有详细的描述，请你根据描述选择比较相关的知识点节点，不需要输出描述
为了方便你理解如何把题目精准匹配知识点节点，我为每个知识点节点都加入了描述，比如生产者消费者 - 多个生产者和消费者通过缓冲区共享数据，-后面的是描述
你只需要在理解的时候使用，输出标签的时候不要输出 - 后面的东西

只能用的知识点节点：knowledge_nodes = ['存储设备-寄存器, 高速缓存, 内存, 磁盘缓存, 固定磁盘, 可移动存储介质', '编译方式-编译, 链接, 装入', '链接方式-静态链接, 装入时动态链接, 运行时动态链接', '装入方式-绝对装入, 可重定位装入, 动态运行时装入', '连续分配-单一连续分配, 固定分区分配, 动态分区分配, 动态重定位分区分配', '分配策略-首次适 应算法(空闲分区地址递增), 循环首次适应算法(循环查找), 最佳适应算法(空闲分区容量递增), 最坏适应算法(空闲分区容量递减)', '离散分配-分页存储管理(有内碎片),  分段存储管理(有外碎片), 段页式存储管理(有内碎片)', '文件定义-具有文件名的一组相关信息的集合', '文件分类-系统文件, 用户文件, 库文件, 只执行文件, 只读文件, 读/写文件, 普通文件, 目录文件, 特殊文件, 源文件, 目标文件, 可执行文件', '层次结构-最高层(文件系统接口), 中间层(对象管理软件), 最底层(存储对象及其属性)', '逻辑结构-无结构文件(流式文件), 顺序文件(存取速度快, 但插入删除困难), 索引文件(检索速度快, 但系统开销大), 索引顺序文件(支持顺序和随机访问)', '目录组织-单级目录, 两级目录, 树形目录, 无环图目录', '索引机制-FCB(文件控制块), 索引节点', '共享方式-索引节点共享, 符号链接共享', '访问控制-访问权和保护域, 访问矩阵', '局部性原理-时间局部性, 空间局部性', '特性-多次性, 对换性, 虚拟性', '分页机制-页表机制, 缺页中断机构, 地址变换机构', '置换算法-最佳置换算法, FIFO, LRU, LFU, Clock', '页面分配-预调页策略, 请求调页策略', '性能问题-抖动, 工作集', '进程定义-进程是程序的运行过程, 是资源分配和调度的基本单位', '进程状态-就绪(等待CPU), 执行(正在运行), 阻塞(等待事件发生)', '进程控制-创建, 终止, 阻塞, 唤醒, 挂起, 激活', '进程组成-PCB(进程控制块), 程序段, 数据段', '进程通信-共享存储, 消息传递, 管道通信', '线程定义-线程是进程内的执行单元, 是处理器调度的基本单位', '实现方式-内核线程(由操作系统管理), 用户级线程(由应用程序管理)', '模式-内核 态, 用户态', '中断与异常-外中断, 内中断', '系统调用-用户程序与操作系统交互的接口', '基本特性-并发(多个事件同时发生), 共享(资源共享), 虚拟(物理资源虚拟化), 异步(进程以不可预测的速度执行)', '核心功能-进程管理(进程控制, 同步, 通信, 调度), 存储管理(内存分配, 保护, 映射, 扩充), 设备管理(缓冲管理, 设备分配, 设备 控制), 文件管理(存储管理, 目录管理, 读写管理, 保护)', '阶段-无操作系统, 单道批处理, 多道批处理, 分时系统, 实时系统, 微机操作系统', '架构类型-模块化, 分层 式, 微内核', 'IO设备-分类方式：按使用特性分为输入设备（键盘、鼠标)、输出设备（打印机、绘图仪)、交互设备（显示器)；按传输速率分为低速设备（键盘、鼠标)、中 速设备（激光打印机)、高速设备（磁带机、磁盘机)', '功能-控制IO设备,实现设备与计算机的数据交换', '设备控制器-组成部分：与处理机的接口,与设备的接口', '通道- 建立独立的IO操作,可能存在瓶颈问题', '轮询IO-过程简单,CPU利用率低', '中断IO-以字节为单位进行IO,提高CPU利用率', 'DMA-直接在IO设备和内存之间传输数据,以数据块为单位', '通道控制-通道程序控制IO设备进行数据传输,一次可传输一组数据块', '设备无关软件-设备独立性：逻辑设备名与物理设备名分离；设备分配考虑因素：设备属性 、分配算法、安全性', 'SPOOLing系统-包含IO井、IO缓冲区、IO进程、井管理程序,特点：提高IO速度,实现虚拟设备功能', '连续组织-优点：顺序访问速度快；缺点：要求空间连续,需提前确定文件大小,动态增长困难', '链接组织-优点：外存利用率高,支持动态增长；缺点：不支持高效直接存取。隐式链接：每个盘块存储下一个盘块的位置指针, 可靠性差。显式链接：物理块信息存储于FAT表,检索速度快,但占用内存空间', '索引组织-优点：支持直接访问,查找速度快,外存利用率高；缺点：索引块占用磁盘空间,索引 块利用率低,索引级数增加导致磁盘访问次数增加。索引方式：单级索引、多级索引、增量式索引', '空闲区表法-连续分配方式,建立空闲表,每个空闲区对应一个表项', '空闲链表法-所有空闲盘区连成一条空闲链', '位示图法-用二进制位表示磁盘盘块的使用情况', '成组链接法-UNIX/Linux文件系统采用的管理方法,将空闲块分组链接', '磁盘缓存-提高磁盘IO效率的缓存机制', '优化方法-提前读,延迟写,优化物理块分布,虚拟盘', 'RAID-廉价磁盘冗余阵列', '容错技术-第一级容错,第二级容错', '后备系统-备用系统 确保数据的可靠性', '集群容错-基于集群系统的容错技术', '资源利用率-最大化系统中处理机和资源的使用', '系统吞吐量-单位时间内完成的作业数', '公平性-防止进程饥饿,合理分配CPU时间', '响应时间-尽可能缩短', '周转时间-尽可能缩短周转时间和带权周转时间', '高级调度-作业调度', '中级调度-内存调度', '低级调度-进程调度', ' 非抢占调度-进程执行完毕前不会被抢占', '抢占调度-调度策略包括优先级、短进程优先、时间片', '先来先服务-按照作业到达的先后顺序调度', '短作业优先-作业越短,优 先级越高', '优先级调度-基于紧迫性赋予不同优先级', '高响应比优先-响应比计算公式：(等待时间 + 要求服务时间) / 要求服务时间', '轮转调度-每个进程每次运行一个 时间片', '多级反馈队列-划分多个就绪队列,优先级不同', '死锁原因-竞争资源,进程推进顺序非法', '死锁必要条件-互斥、请求保持、不可抢占、循环等待', '死锁处理-预防死锁（破坏必要条件),避免死锁（银行家算法),检测死锁（分析资源请求和分配),解除死锁（抢占资源或终止进程)', '临界资源-一次仅供一个进程使用的资源', '临界区- 访问临界资源的代码段', '同步准则-空闲让进、忙则等待、有限等待、让权等待', '软件机制-Peterson算法、关中断', '硬件机制-Test-and-Set指令、Swap指令、信号量机 制（整型信号量、记录型信号量、AND型信号量、信号量集)', '管程-提供同步进程和数据操作的方法', '生产者消费者-多个生产者和消费者通过缓冲区共享数据', '哲学家进餐-避免死锁和饥饿的资源分配问题', '读者写者-控制多个读者和写者对共享资源的访问']
：
重点要求：
- ** 输出格式 **：必须是一个列表，每个列表元素为一个字典，为每个字典加入一个video_word相关知识点列表，请你务必重视，这个知识点列表只能是上面给出的知识点列表里的词，我需要题目与上面知识点节点关联起来，务必重视。


注意，输出必须是完整的一个列表，列表下是一个个完整的字典。不需要输出其他内容.


** 输出示例 **：
[
{"title": "2.1.5_进程通信", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=15","video_word":["进程通信","进程组成"]},
]

"""

video_list += [
    {"title": "2.4.1 死锁的概念", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=38"},
    {"title": "2.4.2 死锁的处理策略—预防死锁", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=39"},
    {"title": "2.4.3 死锁的处理策略—避免死锁", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=40"},
    {"title": "2.4.4 死锁的处理策略—检测和解除", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=41"},
    {"title": "3.1.1_1 内存的基础知识", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=42"},
    {"title": "3.1.1_2 内存管理的概念", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=43"},
    {"title": "3.1.1_4 (选修）覆盖与交换", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=44"},
    {"title": "3.1.2_1 连续分配管理方式", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=45"},
    {"title": "3.1.2_2 动态分区分配算法", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=46"},
    {"title": "3.1.3_1 基本分页存储管理的概念", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=47"},
    {"title": "3.1.3_2 基本地址变换机构", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=48"},
    {"title": "3.1.3_3 具有快表的地址变换机构", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=49"},
    {"title": "3.1.3_4 两级页表", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=50"},
    {"title": "3.1.4 基本分段存储管理方式", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=51"},
    {"title": "3.1.5 段页式管理方式", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=52"},
    {"title": "3.2.1 虚拟内存的基本概念", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=53"},
    {"title": "3.2.2 请求分页管理方式", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=54"},
    {"title": "3.2.4 页面置换算法", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=55"},
    {"title": "3.2.5+3.2.3 页面分配策略", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=56"},
    {"title": "3.2_5_内存映射文件", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=57"},
    {"title": "4.1_1_初识文件管理", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=58"},
    {"title": "4.1_2_文件的逻辑结构", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=59"},
    {"title": "4.1_3_文件目录", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=60"},
    {"title": "4.1_4_文件的物理结构（上）", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=61"},
    {"title": "4.1_4_文件的物理结构（下）", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=62"},
    {"title": "4.1_5_逻辑结构VS物理结构", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=63"},
    {"title": "4.1_6_文件存储空间管理", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=64"},
    {"title": "4.1_7_文件的基本操作", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=65"},
    {"title": "4.1_8_文件共享", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=66"},
    {"title": "4.1_9_文件保护", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=67"},
    {"title": "4.3_1_文件系统的层次结构", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=68"},
    {"title": "4.3_2_文件系统布局", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=69"},
    {"title": "4.3_4_虚拟文件系统", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=70"},
    {"title": "5.1_1_I-O设备的概念和分类", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=71"},
    {"title": "5.1.2_I-O控制器", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=72"},
    {"title": "5.1_3_IO控制方式", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=73"},
    {"title": "5.1_4_I-O软件层次结构", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=74"},
    {"title": "5.1_5_输入输出应用程序接口和驱动程序接口", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=75"},
    {"title": "5.2_1_IO核心子系统", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=76"},
    {"title": "5.2_2_假脱机技术", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=77"},
    {"title": "5.2_3_设备的分配与回收", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=78"},
    {"title": "5.2_4_缓冲区管理", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=79"},
    {"title": "5.3_1_磁盘的结构", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=80"},
    {"title": "5.3_2_磁盘调度算法", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=81"},
    {"title": "5.3_3_减少磁盘延迟时间的方法", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=82"},
    {"title": "5.3_4_磁盘的管理", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=83"},
    {"title": "5.3_5_固态硬盘SSD", "url": "https://www.bilibili.com/video/BV1YE411D7nH?p=84"},
]