"""
应用配置文件
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """应用配置类"""

    # API配置
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # 模型配置
    DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    DEEPSEEK_BASE_URL: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # 应用配置
    USE_DEEPSEEK: bool = os.getenv("USE_DEEPSEEK", "true").lower() == "true"
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "2000"))
    TIMEOUT: int = int(os.getenv("TIMEOUT", "30"))

    # 学习配置
    DEFAULT_LANGUAGE_LEVEL: str = os.getenv("DEFAULT_LANGUAGE_LEVEL", "intermediate")
    MAX_VOCABULARY_PER_SESSION: int = int(os.getenv("MAX_VOCABULARY_PER_SESSION", "50"))
    MAX_CONVERSATION_ROUNDS: int = int(os.getenv("MAX_CONVERSATION_ROUNDS", "10"))

    # 数据库配置
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./english_learning.db")

    # 日志配置
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # 缓存配置
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))
    ENABLE_CACHE: bool = os.getenv("ENABLE_CACHE", "true").lower() == "true"

    @classmethod
    def get_llm_config(cls) -> Dict[str, Any]:
        """获取LLM配置"""
        if cls.USE_DEEPSEEK and cls.DEEPSEEK_API_KEY:
            # 使用 DeepSeek API
            return {
                "model": cls.DEEPSEEK_MODEL,
                "temperature": cls.TEMPERATURE,
                "max_tokens": cls.MAX_TOKENS,
                "openai_api_key": cls.DEEPSEEK_API_KEY,
                "openai_api_base": cls.DEEPSEEK_BASE_URL,
            }
        else:
            # 使用 OpenAI API
            return {
                "model": cls.OPENAI_MODEL,
                "temperature": cls.TEMPERATURE,
                "max_tokens": cls.MAX_TOKENS,
                "api_key": cls.OPENAI_API_KEY,
            }

    @classmethod
    def validate_config(cls) -> bool:
        """验证配置"""
        if cls.USE_DEEPSEEK:
            if not cls.DEEPSEEK_API_KEY or cls.DEEPSEEK_API_KEY in ["your_deepseek_api_key_here", ""]:
                print("警告: DEEPSEEK_API_KEY 未设置或使用默认值")
                print("请在 .env 文件中设置有效的 DeepSeek API 密钥")
                return False
            print(f"使用 DeepSeek API: {cls.DEEPSEEK_MODEL}")
            return True
        else:
            if not cls.OPENAI_API_KEY or cls.OPENAI_API_KEY in ["your_openai_api_key_here", ""]:
                print("警告: OPENAI_API_KEY 未设置或使用默认值")
                print("请在 .env 文件中设置有效的 OpenAI API 密钥")
                return False
            print(f"使用 OpenAI API: {cls.OPENAI_MODEL}")
            return True


# 全局配置实例
settings = Settings()