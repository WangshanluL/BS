# chat.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.utils.websocket_manager import ConnectionManager
from app.utils.ai_client import client
from app.core.log_config import logger
from app.utils.ChatWithRag import rag_and_update_prompt
from app.schemas.chatSchema import GetHistoryRequest, CreateMasterMessage, CreateNewChat
from app.schemas.updateUserPromptSchema import format_video_links,get_last_three_conversation_pairs
from app.services.chat_service import chat_history_service, master_chat_service
from app.services.user_service import user_service
from app.schemas.standardResponse import StandardResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.database_dependency import get_db
import json
from datetime import datetime

router = APIRouter()
manager = ConnectionManager()

@router.get("/")
async def health_check():
    return {"message": "WebSocket服务器已启动"}

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db)):
    await manager.connect(websocket)
    # 为会话创建唯一ID（此处简化为使用WebSocket对象地址）

    # 详细逻辑:首先根据传来的用户id和

    try:
        while True:
            # 接收用户消息
            data = await websocket.receive_text()
            messages = [{"role": "system", "content": f"""
            你是一个专门回答操作系统相关问题的AI助手。提供准确、专业且有深度的回答。
            专业知识领域
            
            操作系统核心概念（进程管理、内存管理、文件系统等）
            主流操作系统（Windows、Linux、macOS、Unix、Android、iOS）
            系统架构、并发与同步、内存虚拟化、文件系统
            系统调用、安全机制、网络协议栈
            性能优化、问题排查与故障分析
            
            回答指南
            
            使用专业术语并提供清晰解释
            根据问题复杂度调整回答深度
            在适当情况下使用代码示例或配置示例
            客观分析各操作系统的优缺点
            提供有条理的故障排查和解决方案
            
            交互原则
            
            保持专业但友好的语气
            对不确定内容诚实表明限制
            避免提供可能导致系统损坏的危险操作
            确保技术内容准确无误
            """}]
            #
            create_user_datetime = datetime.now()
            parsed_data = json.loads(data)
            user_input = parsed_data.get("user_message", "")
            user_id = parsed_data.get("user_id", "")
            chat_id = parsed_data.get("chat_id", "")
            search_options = parsed_data.get("search_options", {})
            #

            # 获取历史聊天记录
            response = await chat_history_service.get_chat_history(db, chat_id, user_id)
            if response.data:
                history_messages = response.data.messages
                history_messages = get_last_three_conversation_pairs(history_messages)
                [messages.append({"role": mess["role"], "content": mess["content"]}) for mess in history_messages]

            #search_options = parsed_data.get("search_options", {})
            # 0 0 0   什么都不需要
            # 0 1 0   只需要互联网信息
            # 1 0 1   rag + 知识图谱查询返回即可
            #
            # 0 0 1  rag 但不需要根据知识图谱增强，只需要把知识图谱查询的题目返回即可
            # 1 0 0 。rag，但只需要知识图谱增强，不需要返回题目
            # 1 1 1  ，0 1 1 ，1 1 0   肯定需要rag
            #
            #
            # ({knowledgeGraph: 0, // 知识图谱检索，默认关闭为0
            #    internet: 0, // 互联网检索，默认关闭为0
            #  learningMaterials: 0 // 学习资料检索，默认关闭为0
            #  });

            LLM_PROMPT, relevant_nodes_links, tavily_results = await rag_and_update_prompt(user_input, search_options)
            learning_materials_enabled = search_options.get("learningMaterials", 0) == 1
            if learning_materials_enabled:
                relevant_topics = [rel for rel in relevant_nodes_links["nodes"] if rel["category"] == 4]
                relevant_video_links = [{"video_title": rel["name"], "video_url": rel["url"]} for rel in
                                        relevant_nodes_links["nodes"] if rel["category"] == 5]
            else:
                relevant_topics = []
                relevant_video_links = []


            logger.info(f"LLM_PROMPT:{LLM_PROMPT}")
            messages.append({"role": "user", "content": LLM_PROMPT})
            await manager.send_json_message({"relevant_nodes_links": relevant_nodes_links, "tavily_results": tavily_results,"relevant_topics":relevant_topics}, websocket)
            try:
                # 创建大模型流式响应
                completion = client.chat.completions.create(
                    model="qwen-omni-turbo",
                    messages=messages,
                    modalities=["text"],
                    stream=True,
                    stream_options={"include_usage": True},
                )

                # 准备AI回复
                ai_response = ""

                # 流式发送响应
                for chunk in completion:
                    if chunk.choices:
                        content = chunk.choices[0].delta.content
                        if content:  # 过滤空内容
                            ai_response += content
                            # 发送消息内容
                            await manager.send_personal_message(ai_response, websocket)

                # 发送结束标记
                create_assistant_datetime = datetime.now()

                if learning_materials_enabled:
                    resultContainVideoStr = format_video_links(ai_response,relevant_video_links)
                    await manager.send_personal_message(resultContainVideoStr,websocket)
                else:
                    await manager.send_personal_message(ai_response + "[END]", websocket)
                cre = CreateMasterMessage(
                    role="user",
                    content=user_input,
                    chat_id=chat_id,
                    user_id=user_id,
                    web_reference=None,
                    gene_reference=None,
                    relevant_topics=None,
                    create_time=create_user_datetime
                )

                cre2 = CreateMasterMessage(
                    role="assistant",
                    content=ai_response,
                    chat_id=chat_id,
                    user_id=user_id,
                    web_reference=tavily_results,
                    gene_reference=relevant_nodes_links,
                    relevant_topics=relevant_topics,
                    create_time=create_assistant_datetime
                )

                await chat_history_service.createMasterMessage(db, cre2)
                await chat_history_service.createMasterMessage(db, cre)


                logger.info(f"ai response :{ai_response}")
            except Exception as e:
                logger.error(f"AI处理异常: {str(e)}")
                await db.rollback()  #不加回滚的话如果这次请求（包含数据库的）失败，没法下次再接受请求
                await manager.send_personal_message(json.dumps({
                    "type": "error",
                    "content": f"处理请求时出错: {str(e)}"
                }), websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info(f"客户端断开连接")
    except Exception as e:
        logger.error(f"WebSocket连接异常: {str(e)}")
    finally:
        # 清理资源
        manager.disconnect(websocket)

@router.post("/chatHistory")
async def getChatHistory(request: GetHistoryRequest, db: AsyncSession = Depends(get_db)):
    chat_id = request.chat_id
    user_id = request.user_id
    response = await chat_history_service.get_chat_history(db, chat_id, user_id)
    return response

@router.post("/newChat")
async def createNewChat(request: CreateNewChat, db: AsyncSession = Depends(get_db)):
    user_id = request.user_id
    user = await user_service.get_by_id(db,user_id)

    if user:
        new_chat = await master_chat_service.create_chat(db, user_id)
        # 若返回的是数据库对象，需要手动转换成json，fastapi没法自动把数据库对象转成json
        chat_dict = {
            "chat_id": new_chat.chat_id,
            "title": new_chat.title,
            "user_id": new_chat.user_id,
            "created_time": new_chat.created_time.isoformat() if hasattr(new_chat.created_time,
                                                                         'isoformat') else new_chat.created_time
        }
        res = StandardResponse(
            code=200,
            message="创建成功",
            data=chat_dict
        )
        return res
    else:
        res = StandardResponse(
            code=405,
            message="未在数据库找到该用户",
            data=[]
        )
        return res
