"""Configuration module for the bot."""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Bot configuration class."""
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # DaData
    DADATA_API_KEY = os.getenv('DADATA_API_KEY', '')
    DADATA_SECRET_KEY = os.getenv('DADATA_SECRET_KEY', '')
    
    # Redis
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
    
    # Cache
    CACHE_TTL = int(os.getenv('CACHE_TTL', 3600))
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS = int(os.getenv('RATE_LIMIT_REQUESTS', 10))
    RATE_LIMIT_PERIOD = int(os.getenv('RATE_LIMIT_PERIOD', 60))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError('TELEGRAM_BOT_TOKEN is required')
        if not cls.DADATA_API_KEY:
            raise ValueError('DADATA_API_KEY is required')
        return True


config = Config()
