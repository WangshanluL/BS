from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"

    class Config:
        env_file = ".env"
settings = Settings()