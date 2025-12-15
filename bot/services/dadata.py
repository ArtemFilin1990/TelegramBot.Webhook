"""DaData API service for company information."""
import logging
from typing import Optional, Dict, Any
import requests
from config import config
from bot.utils.cache import cache

logger = logging.getLogger(__name__)


class DaDataService:
    """Service for interacting with DaData API."""
    
    BASE_URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs"
    
    def __init__(self):
        """Initialize DaData service."""
        self.api_key = config.DADATA_API_KEY
        self.secret_key = config.DADATA_SECRET_KEY
        self.headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def find_by_inn(self, inn: str) -> Optional[Dict[str, Any]]:
        """Find company by INN."""
        cache_key = f"company:inn:{inn}"
        cached = cache.get(cache_key)
        if cached:
            logger.info(f"Cache hit for INN: {inn}")
            return cached
        
        try:
            url = f"{self.BASE_URL}/findById/party"
            data = {"query": inn}
            
            response = requests.post(url, json=data, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result.get('suggestions'):
                company_data = result['suggestions'][0]
                cache.set(cache_key, company_data)
                return company_data
            
            return None
        except Exception as e:
            logger.error(f"Error finding company by INN {inn}: {e}")
            return None
    
    def find_by_ogrn(self, ogrn: str) -> Optional[Dict[str, Any]]:
        """Find company by OGRN."""
        cache_key = f"company:ogrn:{ogrn}"
        cached = cache.get(cache_key)
        if cached:
            logger.info(f"Cache hit for OGRN: {ogrn}")
            return cached
        
        try:
            url = f"{self.BASE_URL}/findById/party"
            data = {"query": ogrn}
            
            response = requests.post(url, json=data, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result.get('suggestions'):
                company_data = result['suggestions'][0]
                cache.set(cache_key, company_data)
                return company_data
            
            return None
        except Exception as e:
            logger.error(f"Error finding company by OGRN {ogrn}: {e}")
            return None
    
    def search_company(self, query: str) -> list:
        """Search companies by query."""
        try:
            url = f"{self.BASE_URL}/suggest/party"
            data = {"query": query, "count": 10}
            
            response = requests.post(url, json=data, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            return result.get('suggestions', [])
        except Exception as e:
            logger.error(f"Error searching companies: {e}")
            return []


# Global service instance
dadata_service = DaDataService()
