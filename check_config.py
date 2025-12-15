"""
Configuration checker script.

Validates that all required environment variables are set
and API keys are working correctly.
"""
import sys
from config import config


def check_env_vars():
    """Check if all required environment variables are set."""
    print("=" * 60)
    print("Environment Variables Check")
    print("=" * 60)
    
    required = {
        'TELEGRAM_BOT_TOKEN': config.TELEGRAM_BOT_TOKEN,
        'OPENAI_API_KEY': config.OPENAI_API_KEY,
        'OPENAI_ASSISTANT_ID': config.OPENAI_ASSISTANT_ID,
        'DADATA_API_KEY': config.DADATA_API_KEY,
        'DADATA_SECRET_KEY': config.DADATA_SECRET_KEY,
    }
    
    all_set = True
    for key, value in required.items():
        status = "✅" if value else "❌"
        print(f"{status} {key}: {'Set' if value else 'NOT SET'}")
        if not value:
            all_set = False
    
    print()
    return all_set


def check_telegram():
    """Check Telegram Bot API connection."""
    print("=" * 60)
    print("Telegram Bot API Check")
    print("=" * 60)
    
    try:
        import requests
        token = config.TELEGRAM_BOT_TOKEN
        url = f"https://api.telegram.org/bot{token}/getMe"
        
        response = requests.get(url, timeout=10)
        result = response.json()
        
        if result.get('ok'):
            bot_info = result.get('result', {})
            print(f"✅ Bot connected successfully")
            print(f"   Username: @{bot_info.get('username')}")
            print(f"   Name: {bot_info.get('first_name')}")
            return True
        else:
            print(f"❌ Error: {result.get('description')}")
            return False
            
    except Exception as e:
        print(f"❌ Error connecting to Telegram: {e}")
        return False


def check_openai():
    """Check OpenAI API connection."""
    print("\n" + "=" * 60)
    print("OpenAI API Check")
    print("=" * 60)
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=config.OPENAI_API_KEY)
        
        # Test API key
        models = client.models.list()
        print(f"✅ OpenAI API key is valid")
        
        # Check Assistant
        if config.OPENAI_ASSISTANT_ID:
            try:
                assistant = client.beta.assistants.retrieve(config.OPENAI_ASSISTANT_ID)
                print(f"✅ Assistant found: {assistant.name}")
            except Exception as e:
                print(f"❌ Assistant not found: {e}")
                return False
        else:
            print(f"⚠️  Assistant ID not set. Run: python setup.py create-assistant")
            return False
        
        # Check Vector Store
        if config.OPENAI_VECTOR_STORE_ID:
            try:
                vs = client.beta.vector_stores.retrieve(config.OPENAI_VECTOR_STORE_ID)
                print(f"✅ Vector Store found: {vs.name}")
            except Exception as e:
                print(f"❌ Vector Store not found: {e}")
                return False
        else:
            print(f"⚠️  Vector Store ID not set. Run: python setup.py create-assistant")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error connecting to OpenAI: {e}")
        return False


def check_dadata():
    """Check DaData API connection."""
    print("\n" + "=" * 60)
    print("DaData API Check")
    print("=" * 60)
    
    try:
        import requests
        
        url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party"
        headers = {
            "Authorization": f"Token {config.DADATA_API_KEY}",
            "Content-Type": "application/json",
        }
        data = {"query": "7707083893"}  # Сбербанк
        
        response = requests.post(url, json=data, headers=headers, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        if result.get('suggestions'):
            company = result['suggestions'][0]
            print(f"✅ DaData API is working")
            print(f"   Test query: ИНН 7707083893")
            print(f"   Found: {company.get('value', 'N/A')}")
            return True
        else:
            print(f"❌ No results from DaData")
            return False
            
    except Exception as e:
        print(f"❌ Error connecting to DaData: {e}")
        return False


def check_webhook():
    """Check webhook status."""
    print("\n" + "=" * 60)
    print("Webhook Check")
    print("=" * 60)
    
    try:
        import requests
        token = config.TELEGRAM_BOT_TOKEN
        url = f"https://api.telegram.org/bot{token}/getWebhookInfo"
        
        response = requests.get(url, timeout=10)
        result = response.json()
        
        if result.get('ok'):
            info = result.get('result', {})
            webhook_url = info.get('url', '')
            
            if webhook_url:
                print(f"✅ Webhook is set")
                print(f"   URL: {webhook_url}")
                print(f"   Pending updates: {info.get('pending_update_count', 0)}")
                
                if info.get('last_error_message'):
                    print(f"⚠️  Last error: {info.get('last_error_message')}")
                    print(f"   Error date: {info.get('last_error_date')}")
                    return False
                return True
            else:
                print(f"⚠️  Webhook is not set")
                print(f"   Run: python setup.py set-webhook <your-url>/api/webhook")
                return False
        else:
            print(f"❌ Error: {result.get('description')}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking webhook: {e}")
        return False


def main():
    """Run all checks."""
    print("\n")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║        Telegram Bot Configuration Checker               ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    
    checks = {
        'Environment Variables': check_env_vars(),
        'Telegram Bot API': check_telegram(),
        'OpenAI API': check_openai(),
        'DaData API': check_dadata(),
        'Webhook': check_webhook(),
    }
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    all_passed = True
    for check_name, passed in checks.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {check_name}")
        if not passed:
            all_passed = False
    
    print()
    
    if all_passed:
        print("🎉 All checks passed! Your bot is ready to run.")
        print()
        print("Next steps:")
        print("1. Deploy to Vercel: vercel --prod")
        print("2. Set webhook: python setup.py set-webhook <your-url>/api/webhook")
        print("3. Test your bot in Telegram")
        sys.exit(0)
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print()
        print("Need help?")
        print("- Check README.md for detailed instructions")
        print("- See QUICKSTART.md for quick setup guide")
        sys.exit(1)


if __name__ == "__main__":
    main()
