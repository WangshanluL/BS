from pydantic_settings import BaseSettings
import os
import sys
import inspect
from pathlib import Path
from dotenv import load_dotenv


# 获取 main.py 所在的目录
def get_main_directory():
    # 方法1: 如果直接运行脚本，使用 __file__
    if __name__ == "__main__" and '__file__' in globals():
        return os.path.dirname(os.path.abspath(__file__))

    # 方法2: 尝试获取调用栈中主模块的文件路径
    try:
        main_module = sys.modules['__main__']
        if hasattr(main_module, '__file__'):
            return os.path.dirname(os.path.abspath(main_module.__file__))
    except (KeyError, AttributeError):
        pass

    # 方法3: 使用 sys.argv[0]，但这在某些情况下可能不可靠
    if len(sys.argv) > 0 and os.path.isfile(sys.argv[0]):
        return os.path.dirname(os.path.abspath(sys.argv[0]))

    # 方法4: 找到包含 main.py 的目录
    # 遍历调用栈查找可能的入口点
    for frame_info in inspect.stack():
        if frame_info.filename.endswith('main.py'):
            return os.path.dirname(os.path.abspath(frame_info.filename))

    # 方法5: 如果所有方法都失败，则尝试使用当前工作目录
    current_dir = os.getcwd()
    if os.path.exists(os.path.join(current_dir, 'main.py')):
        return current_dir

    # 如果找不到合适的目录，返回当前工作目录并打印警告
    #print("⚠️ Warning: Could not reliably determine main.py location. Using current directory.")
    return current_dir


# 获取基础目录并构建 .env 文件路径
BASE_DIR = get_main_directory()
ENV_PATH = os.path.join(BASE_DIR, ".env")

# 先用 dotenv 加载环境变量
if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)
    print(f"✅ Loaded environment variables from {ENV_PATH}")
else:
    #print(f"⚠️ Warning: .env file not found at {ENV_PATH}")
    # 尝试向上查找一级目录
    parent_env = os.path.join(os.path.dirname(BASE_DIR), ".env")
    if os.path.exists(parent_env):
        load_dotenv(parent_env)
        ENV_PATH = parent_env
        print(f"✅ Found and loaded .env from parent directory: {ENV_PATH}")


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str
    DASHSCOPE_API_KEY: str
    NEO4J_USER: str
    NEO4J_PASSWORD: str
    NEO4J_URL: str

    class Config:
        env_file = ENV_PATH  # 使用确定的绝对路径
        env_file_encoding = 'utf-8'  # 确保正确处理UTF-8编码


settings = Settings()