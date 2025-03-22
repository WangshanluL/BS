import asyncio
from app.utils.RagFromNeo4j import ragFromNeo4j
from app.utils.RagFromTavily import search_tavily
from app.schemas.updateUserPromptSchema import get_os_qa_prompt
from app.utils.ChatWithRag import rag_and_update_prompt  # 请替换为实际的模块路径

# 测试用例1: 所有选项都启用
async def test_case_1():
    print("测试用例1: 所有选项都启用")
    prompt = "如何使用Python处理大数据？"
    search_options = {
        "knowledgeGraph": 1,
        "internet": 1,
        "learningMaterials": 1
    }
    result = await rag_and_update_prompt(prompt, search_options)
    print(f"LLM提示词: {result[0]}...")
    print(f"知识图谱节点数量: {len(result[1])}")
    print(f"互联网搜索结果数量: {len(result[2])}")
    print("-------------------")

# 测试用例2: 只启用知识图谱
async def test_case_2():
    print("测试用例2: 只启用知识图谱")
    prompt = "Python中的装饰器如何使用？"
    search_options = {
        "knowledgeGraph": 1,
        "internet": 0,
        "learningMaterials": 0
    }
    result = await rag_and_update_prompt(prompt, search_options)
    print(f"LLM提示词: {result[0]}...")
    print(f"知识图谱节点数量: {len(result[1])}")
    print(f"互联网搜索结果数量: {len(result[2])}")
    print("-------------------")

# 测试用例3: 只启用互联网搜索
async def test_case_3():
    print("测试用例3: 只启用互联网搜索")
    prompt = "最新的AI技术发展趋势是什么？"
    search_options = {
        "knowledgeGraph": 0,
        "internet": 1,
        "learningMaterials": 0
    }
    result = await rag_and_update_prompt(prompt, search_options)
    print(f"LLM提示词: {result[0]}...")
    print(f"知识图谱节点数量: {len(result[1])}")
    print(f"互联网搜索结果数量: {len(result[2])}")
    print("-------------------")

# 测试用例4: 只启用学习材料
async def test_case_4():
    print("测试用例4: 只启用学习材料")
    prompt = "深度学习的基本原理是什么？"
    search_options = {
        "knowledgeGraph": 0,
        "internet": 0,
        "learningMaterials": 1
    }
    result = await rag_and_update_prompt(prompt, search_options)
    print(f"LLM提示词: {result[0]}...")
    print(f"知识图谱节点数量: {len(result[1])}")
    print(f"互联网搜索结果数量: {len(result[2])}")
    print("-------------------")

# 测试用例5: 所有选项都禁用
async def test_case_5():
    print("测试用例5: 所有选项都禁用")
    prompt = "你好，请问你是谁？"
    search_options = {
        "knowledgeGraph": 0,
        "internet": 0,
        "learningMaterials": 0
    }
    result = await rag_and_update_prompt(prompt, search_options)
    print(f"LLM提示词: {result[0]}...")
    print(f"知识图谱节点数量: {len(result[1])}")
    print(f"互联网搜索结果数量: {len(result[2])}")
    print("-------------------")

# 运行所有测试用例
async def run_all_tests():
    await test_case_1()
    await test_case_2()
    await test_case_3()
    await test_case_4()
    await test_case_5()

# 执行测试
if __name__ == "__main__":
    asyncio.run(run_all_tests())