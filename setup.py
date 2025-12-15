"""
Setup script for OpenAI Assistant and Telegram Webhook.

Run this script to:
1. Create OpenAI Assistant with proper instructions
2. Create Vector Store for memory
3. Set up Telegram webhook
"""
import asyncio
import sys
from openai import OpenAI
import requests
from config import config

# Assistant instructions
ASSISTANT_INSTRUCTIONS = """
Ты - помощник для анализа данных о российских компаниях.

КРИТИЧЕСКИ ВАЖНО:
1. Используй ТОЛЬКО данные из MCP DaData, которые тебе предоставлены
2. ЗАПРЕЩЕНО додумывать, предполагать или использовать внутренние знания модели
3. Если данных нет - пиши "нет данных"
4. Никакого скоринга, рейтингов, оценок надёжности

ФОРМАТ ОТВЕТОВ:
- iOS-стиль с использованием символов для оформления
- Структурированная информация с разделителями
- Используй эмодзи: 🏢 📊 💰 📍 👤 👥 ⚖️ 🏛
- Блоки обрамляй символами ┏━━━┓ и ┗━━━┛

ЭКРАНЫ:
1. Краткий отчёт: основная информация, статус, руководство
2. Финансы: уставный капитал, финансовые показатели (если есть)
3. Реквизиты: ИНН, ОГРН, КПП, даты регистрации
4. Адрес: юридический адрес, индекс, регион
5. История - Директора: текущий руководитель, история смены
6. История - Учредители: список учредителей с долями
7. История - Адреса: история изменения адресов
8. История - ОКВЭД: основной и дополнительные виды деятельности

СТРОГИЕ ПРАВИЛА:
- Только факты из предоставленных данных
- Если поле пустое или отсутствует - "нет данных"
- Не давай советов, рекомендаций, оценок
- Не интерпретируй данные - только показывай их
"""


def create_assistant():
    """Create OpenAI Assistant."""
    print("Creating OpenAI Assistant...")
    
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    
    try:
        # Create vector store first
        vector_store = client.beta.vector_stores.create(
            name="Egrul Bot Memory",
            expires_after={
                "anchor": "last_active_at",
                "days": 7
            }
        )
        
        print(f"✅ Vector Store created: {vector_store.id}")
        
        # Create assistant
        assistant = client.beta.assistants.create(
            name="Egrul Bot Assistant",
            instructions=ASSISTANT_INSTRUCTIONS,
            model="gpt-4-turbo-preview",
            tools=[
                {"type": "file_search"}
            ],
            tool_resources={
                "file_search": {
                    "vector_store_ids": [vector_store.id]
                }
            }
        )
        
        print(f"✅ Assistant created: {assistant.id}")
        print(f"\nAdd these to your .env file:")
        print(f"OPENAI_ASSISTANT_ID={assistant.id}")
        print(f"OPENAI_VECTOR_STORE_ID={vector_store.id}")
        
        return assistant.id, vector_store.id
        
    except Exception as e:
        print(f"❌ Error creating assistant: {e}")
        sys.exit(1)


def setup_webhook(webhook_url: str):
    """Set up Telegram webhook."""
    print(f"\nSetting up Telegram webhook: {webhook_url}")
    
    token = config.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/setWebhook"
    
    try:
        response = requests.post(url, json={"url": webhook_url})
        result = response.json()
        
        if result.get('ok'):
            print(f"✅ Webhook set successfully")
            print(f"URL: {webhook_url}")
        else:
            print(f"❌ Error setting webhook: {result.get('description')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def get_webhook_info():
    """Get current webhook info."""
    print("\nChecking current webhook info...")
    
    token = config.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/getWebhookInfo"
    
    try:
        response = requests.get(url)
        result = response.json()
        
        if result.get('ok'):
            info = result.get('result', {})
            print(f"Current webhook URL: {info.get('url', 'Not set')}")
            print(f"Pending updates: {info.get('pending_update_count', 0)}")
            if info.get('last_error_message'):
                print(f"Last error: {info.get('last_error_message')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main setup function."""
    print("=" * 60)
    print("OpenAI Assistant & Telegram Webhook Setup")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "create-assistant":
            create_assistant()
        
        elif command == "set-webhook":
            if len(sys.argv) < 3:
                print("Usage: python setup.py set-webhook <webhook_url>")
                print("Example: python setup.py set-webhook https://your-app.vercel.app/api/webhook")
                sys.exit(1)
            
            webhook_url = sys.argv[2]
            setup_webhook(webhook_url)
        
        elif command == "webhook-info":
            get_webhook_info()
        
        elif command == "full-setup":
            # Full setup
            assistant_id, vector_store_id = create_assistant()
            
            if len(sys.argv) >= 3:
                webhook_url = sys.argv[2]
                setup_webhook(webhook_url)
            else:
                print("\n⚠️ Webhook URL not provided. Run later with:")
                print("python setup.py set-webhook <your-vercel-url>/api/webhook")
        
        else:
            print(f"Unknown command: {command}")
            print_usage()
    
    else:
        print_usage()


def print_usage():
    """Print usage information."""
    print("\nUsage:")
    print("  python setup.py create-assistant          # Create OpenAI Assistant and Vector Store")
    print("  python setup.py set-webhook <url>         # Set Telegram webhook")
    print("  python setup.py webhook-info              # Get current webhook info")
    print("  python setup.py full-setup [webhook_url]  # Complete setup")
    print("\nExample:")
    print("  python setup.py full-setup https://your-app.vercel.app/api/webhook")


if __name__ == "__main__":
    main()
