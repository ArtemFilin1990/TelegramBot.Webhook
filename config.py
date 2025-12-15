"""Configuration module for the bot."""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Bot configuration class."""
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_WEBHOOK_URL = os.getenv('TELEGRAM_WEBHOOK_URL', '')
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_ASSISTANT_ID = os.getenv('OPENAI_ASSISTANT_ID', '')
    OPENAI_VECTOR_STORE_ID = os.getenv('OPENAI_VECTOR_STORE_ID', '')
    
    # MCP DaData
    MCP_DADATA_URL = os.getenv('MCP_DADATA_URL', 'https://mcp.dadata.ru/mcp')
    DADATA_API_KEY = os.getenv('DADATA_API_KEY', '')
    DADATA_SECRET_KEY = os.getenv('DADATA_SECRET_KEY', '')
    
    # Vercel
    VERCEL_ENV = os.getenv('VERCEL_ENV', 'development')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError('TELEGRAM_BOT_TOKEN is required')
        if not cls.OPENAI_API_KEY:
            raise ValueError('OPENAI_API_KEY is required')
        if not cls.OPENAI_ASSISTANT_ID:
            raise ValueError('OPENAI_ASSISTANT_ID is required')
        if not cls.DADATA_API_KEY:
            raise ValueError('DADATA_API_KEY is required')
        return True


config = Config()
