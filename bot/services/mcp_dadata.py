"""MCP DaData integration service - STRICT data source."""
import logging
from typing import Optional, Dict, Any
import requests
from config import config

logger = logging.getLogger(__name__)


class MCPDaDataService:
    """
    Service for MCP DaData integration.
    
    CRITICAL: This is the ONLY source of company data.
    No hallucination, no assumptions - only factual data from MCP.
    """
    
    def __init__(self):
        """Initialize MCP DaData service."""
        self.mcp_url = config.MCP_DADATA_URL
        self.api_key = config.DADATA_API_KEY
        self.secret_key = config.DADATA_SECRET_KEY
        
        # DaData API endpoints
        self.base_url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs"
        self.headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def find_by_inn(self, inn: str) -> Optional[Dict[str, Any]]:
        """
        Find company by INN through MCP DaData.
        
        Returns ONLY factual data from DaData.
        """
        try:
            url = f"{self.base_url}/findById/party"
            data = {"query": inn}
            
            logger.info(f"Querying MCP DaData for INN: {inn}")
            response = requests.post(url, json=data, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            result = response.json()
            if result.get('suggestions'):
                company_data = result['suggestions'][0]
                logger.info(f"Found company via MCP DaData: {inn}")
                return self._normalize_company_data(company_data)
            
            logger.warning(f"Company not found for INN: {inn}")
            return None
            
        except Exception as e:
            logger.error(f"Error querying MCP DaData for INN {inn}: {e}")
            return None
    
    def find_by_ogrn(self, ogrn: str) -> Optional[Dict[str, Any]]:
        """
        Find company by OGRN through MCP DaData.
        
        Returns ONLY factual data from DaData.
        """
        try:
            url = f"{self.base_url}/findById/party"
            data = {"query": ogrn}
            
            logger.info(f"Querying MCP DaData for OGRN: {ogrn}")
            response = requests.post(url, json=data, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            result = response.json()
            if result.get('suggestions'):
                company_data = result['suggestions'][0]
                logger.info(f"Found company via MCP DaData: {ogrn}")
                return self._normalize_company_data(company_data)
            
            logger.warning(f"Company not found for OGRN: {ogrn}")
            return None
            
        except Exception as e:
            logger.error(f"Error querying MCP DaData for OGRN {ogrn}: {e}")
            return None
    
    def _normalize_company_data(self, raw_data: Dict) -> Dict[str, Any]:
        """
        Normalize company data from DaData.
        
        Returns structured data with "нет данных" for missing fields.
        """
        data = raw_data.get('data', {})
        
        normalized = {
            'raw': raw_data,  # Keep raw data for reference
            'data': {
                # Basic info
                'inn': data.get('inn', 'нет данных'),
                'ogrn': data.get('ogrn', 'нет данных'),
                'kpp': data.get('kpp', 'нет данных'),
                
                # Names
                'name': {
                    'full': data.get('name', {}).get('full_with_opf', 'нет данных'),
                    'short': data.get('name', {}).get('short_with_opf', 'нет данных'),
                    'latin': data.get('name', {}).get('latin', 'нет данных'),
                },
                
                # Status
                'state': {
                    'status': data.get('state', {}).get('status', 'нет данных'),
                    'registration_date': data.get('state', {}).get('registration_date', 'нет данных'),
                    'liquidation_date': data.get('state', {}).get('liquidation_date', 'нет данных'),
                },
                
                # Management
                'management': {
                    'name': data.get('management', {}).get('name', 'нет данных'),
                    'post': data.get('management', {}).get('post', 'нет данных'),
                },
                
                # Founders
                'founders': data.get('founders', []) or [],
                
                # Address
                'address': {
                    'value': data.get('address', {}).get('value', 'нет данных'),
                    'postal_code': data.get('address', {}).get('data', {}).get('postal_code', 'нет данных'),
                    'region': data.get('address', {}).get('data', {}).get('region', 'нет данных'),
                    'city': data.get('address', {}).get('data', {}).get('city', 'нет данных'),
                },
                
                # OKVED
                'okved': data.get('okved', 'нет данных'),
                'okved_type': data.get('okved_type', 'нет данных'),
                'okveds': data.get('okveds', []) or [],
                
                # Financial
                'capital': {
                    'value': data.get('capital', {}).get('value', 'нет данных'),
                    'currency': data.get('capital', {}).get('currency', 'нет данных'),
                },
                
                # Finance (if available)
                'finance': data.get('finance', {}) or {'note': 'нет данных'},
                
                # Employees
                'employees': data.get('employees', 'нет данных'),
                
                # Type
                'type': data.get('type', 'нет данных'),
                'opf': data.get('opf', {}).get('full', 'нет данных'),
            }
        }
        
        return normalized
    
    def get_company_finances(self, inn: str) -> Dict[str, Any]:
        """
        Get financial data for company.
        
        Note: Financial data may require paid DaData subscription.
        """
        company = self.find_by_inn(inn)
        if not company:
            return {'error': 'Company not found'}
        
        finance = company.get('data', {}).get('finance', {})
        if not finance or finance.get('note') == 'нет данных':
            return {
                'note': 'Финансовые данные требуют расширенной подписки DaData',
                'available': False
            }
        
        return {
            'available': True,
            'data': finance
        }


# Global service instance
mcp_dadata_service = MCPDaDataService()
