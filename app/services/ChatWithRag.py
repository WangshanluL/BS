import asyncio
from typing import Dict, Any, Optional
from app.services.RagFromNeo4j import ragFromNeo4j
from app.services.RagFromTavily import search_tavily
async def enhanced_prompt_with_context(prompt: str):
    """
    """
    # Create tasks for both searches to run concurrently
    neo4j_task = asyncio.create_task(ragFromNeo4j(prompt))
    tavily_task = asyncio.create_task(search_tavily(prompt))

    # Wait for both tasks to complete
    tavily_results, neo4j_results = await asyncio.gather(tavily_task, neo4j_task)
    str_corpus, relevant_nodes_links = neo4j_results
    LLM_PROMPT = f"""
    用户需求为:{prompt}
    
    请你根据你的知识以及你检索到的信息回答用户的问题，
    
    **必须遵守的生成协议（❗违反将导致重大故障❗）**    
    1. 如果你在最终回应用户的时候，请你以[citation:1]格式引用，这个引用代表某句话引用了网页1的内容。同理如下：Aesop品牌通过独特的设计美学成长为百亿价值的品牌[citation:2]代表引用了网页2的内容,
    2. 请你注意在引用过程中应该把引用标签放在回应的某句话的后面。当且仅当你回答中参考了网页几的信息才在回答的句子中加上引用标签[citation:x]，千万不要乱加引用标签.
    
    1.你从知识图谱里检索到的信息为：{str_corpus}
    2.你从互联网上检索到的信息为:{tavily_results["contents"]} 
       
    """


    return LLM_PROMPT,relevant_nodes_links,tavily_results["results"]


# Example usage
async def example_usage():
    user_prompt = "什么是抖动（thrashing），为什么会发生？如何避免？"
    enhanced = await enhanced_prompt_with_context(user_prompt)
    # Now you can use the enhanced prompt with your LLM
    # llm_response = await call_llm_with_prompt(enhanced)
    return enhanced