"""OpenAI Assistant and Vector Store service."""
import logging
from typing import Dict, Any, Optional, List
from openai import OpenAI
from config import config

logger = logging.getLogger(__name__)


class AssistantService:
    """Service for OpenAI Assistant with Vector Store."""
    
    def __init__(self):
        """Initialize OpenAI Assistant service."""
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.assistant_id = config.OPENAI_ASSISTANT_ID
        self.vector_store_id = config.OPENAI_VECTOR_STORE_ID
        
        # Thread management (in-memory for serverless)
        self.threads = {}
    
    def get_or_create_thread(self, user_id: int) -> str:
        """Get or create thread for user."""
        if user_id not in self.threads:
            try:
                thread = self.client.beta.threads.create()
                self.threads[user_id] = thread.id
                logger.info(f"Created new thread for user {user_id}: {thread.id}")
            except Exception as e:
                logger.error(f"Error creating thread: {e}")
                raise
        
        return self.threads[user_id]
    
    def store_in_vector_store(self, user_id: int, content: str, metadata: Dict[str, Any]):
        """Store content in vector store for retrieval."""
        try:
            # Create a file with content
            file = self.client.files.create(
                file=content.encode('utf-8'),
                purpose='assistants'
            )
            
            # Add to vector store
            self.client.beta.vector_stores.files.create(
                vector_store_id=self.vector_store_id,
                file_id=file.id
            )
            
            logger.info(f"Stored content in vector store for user {user_id}")
        except Exception as e:
            logger.error(f"Error storing in vector store: {e}")
    
    def query_company(self, user_id: int, query: str, company_data: Optional[Dict] = None) -> str:
        """
        Query assistant about company with retrieval from vector store.
        
        Args:
            user_id: Telegram user ID
            query: User query (e.g., "show finances", "directors history")
            company_data: Company data from MCP DaData
        
        Returns:
            Formatted response from assistant
        """
        try:
            thread_id = self.get_or_create_thread(user_id)
            
            # Prepare message with company data
            message_content = query
            if company_data:
                message_content += f"\n\nCompany Data from MCP DaData:\n{str(company_data)}"
            
            # Create message
            self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=message_content
            )
            
            # Run assistant with retrieval
            run = self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=self.assistant_id,
                tools=[{"type": "file_search"}]
            )
            
            # Wait for completion
            while run.status in ['queued', 'in_progress']:
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run.id
                )
            
            if run.status == 'completed':
                # Get messages
                messages = self.client.beta.threads.messages.list(
                    thread_id=thread_id
                )
                
                # Get latest assistant message
                for message in messages.data:
                    if message.role == 'assistant':
                        content = message.content[0].text.value
                        
                        # Store response in vector store
                        self.store_in_vector_store(
                            user_id,
                            f"Query: {query}\nResponse: {content}",
                            {"user_id": user_id, "type": "query_response"}
                        )
                        
                        return content
                
                return "Не удалось получить ответ от ассистента."
            else:
                logger.error(f"Run failed with status: {run.status}")
                return "Произошла ошибка при обработке запроса."
                
        except Exception as e:
            logger.error(f"Error querying assistant: {e}")
            return f"Ошибка: {str(e)}"
    
    def format_screen(self, user_id: int, screen_type: str, company_data: Dict) -> str:
        """
        Format specific screen using assistant.
        
        Args:
            user_id: Telegram user ID
            screen_type: Type of screen (brief, finances, requisites, etc.)
            company_data: Company data from MCP DaData
        
        Returns:
            Formatted screen content
        """
        screen_prompts = {
            'brief': 'Создай краткий отчёт о компании в iOS-стиле. Используй только данные из MCP DaData. Если данных нет - пиши "нет данных".',
            'finances': 'Покажи финансовую информацию компании. Только факты из MCP DaData.',
            'requisites': 'Покажи реквизиты компании (ИНН, ОГРН, КПП и т.д.).',
            'address': 'Покажи адресную информацию компании.',
            'directors': 'Покажи историю директоров компании.',
            'founders': 'Покажи информацию об учредителях компании.',
            'addresses_history': 'Покажи историю адресов компании.',
            'okved': 'Покажи виды деятельности (ОКВЭД) компании.',
        }
        
        prompt = screen_prompts.get(screen_type, 'Покажи информацию о компании.')
        return self.query_company(user_id, prompt, company_data)
    
    def search_vector_store(self, query: str) -> List[Dict]:
        """Search vector store for relevant content."""
        try:
            # This is a simplified version - in production, implement proper vector search
            # For now, return empty list as vector store search requires more setup
            return []
        except Exception as e:
            logger.error(f"Error searching vector store: {e}")
            return []


# Global service instance
assistant_service = AssistantService()
