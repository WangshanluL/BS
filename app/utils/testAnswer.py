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


# 示例用法
if __name__ == "__main__":
    # 假设这是你的历史消息列表
    from collections import namedtuple

    Message = namedtuple('Message', ['role', 'content'])

    history_messages = [
        Message(role="user", content="你好"),
        Message(role="assistant", content="你好！有什么我能帮助你的吗？"),
        Message(role="user", content="Python如何处理JSON？"),
        Message(role="assistant", content="Python可以使用json模块处理JSON数据..."),
        Message(role="user", content="给我一个例子"),
        Message(role="assistant", content="以下是一个Python处理JSON的例子..."),
        Message(role="user", content="谢谢"),
        Message(role="assistant", content="不客气，随时为您服务！"),
        # 可能有一些不成对的消息
        Message(role="system", content="系统消息"),
        Message(role="user", content="另一个问题")
    ]

    # 获取最后三组对话
    result = get_last_three_conversation_pairs(history_messages)

    # 打印结果
    for msg in result:
        print(f"{msg['role']}: {msg['content'][:20]}...")