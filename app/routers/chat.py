# chat.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.websocket_manager import ConnectionManager
from app.utils.ai_client import client
from app.core.log_config import logger
from app.services.ChatWithRag import enhanced_prompt_with_context

import json
import asyncio

router = APIRouter()
manager = ConnectionManager()

@router.get("/")
async def health_check():
    return {"message": "WebSocket服务器已启动"}

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)
    # 为会话创建唯一ID（此处简化为使用WebSocket对象地址）


    # 详细逻辑:首先根据传来的用户id和


    try:
        while True:
            # 接收用户消息
            data = await websocket.receive_text()
            messages = [{"role":"system","content":f"""
            """}]
            # 这个是需要从数据库里获取的，后面再写
            parsed_data = json.loads(data)
            user_input = parsed_data.get("message", "")
            LLM_PROMPT, relevant_nodes_links, tavily_results = await enhanced_prompt_with_context(user_input)
            logger.info(f"LLM_PROMPT:{LLM_PROMPT}")
            messages.append({"role":"user","content":LLM_PROMPT})
            await manager.send_json_message({"relevant_nodes_links":relevant_nodes_links,"tavily_results":tavily_results},websocket)
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
                await manager.send_personal_message("[END]", websocket)
                logger.info(f"ai response :{ai_response}")
            except Exception as e:
                logger.error(f"AI处理异常: {str(e)}")
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

