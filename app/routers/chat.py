# chat.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.websocket_manager import ConnectionManager
from app.utils.ai_client import client
from app.core.logging import logger
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

    try:
        while True:
            # 接收用户消息
            data = await websocket.receive_text()
            messages = [{"role":"system","content":f"""
            你是一名大学生，帮我输出搞笑文案

            """}]
            try:
                # 尝试解析JSON，支持更复杂的前端请求
                parsed_data = json.loads(data)
                user_input = parsed_data.get("message", "")
                # 可以添加其他参数，例如模型选择、历史清除等
                # clear_history = parsed_data.get("clearHistory", False)
                messages.append({"role":"user","content":user_input})



            except json.JSONDecodeError:
                # 如果不是JSON，就当作纯文本处理
                user_input = data


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
                            await manager.send_personal_message(content, websocket)


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

