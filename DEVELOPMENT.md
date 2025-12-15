# Локальное тестирование и разработка

## Настройка локального окружения

### 1. Установка зависимостей

```bash
# Создайте виртуальное окружение
python -m venv venv

# Активируйте его
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Установите зависимости
pip install -r requirements.txt
```

### 2. Настройка .env

```bash
cp .env.example .env
```

Заполните `.env`:

```env
TELEGRAM_BOT_TOKEN=your_bot_token
OPENAI_API_KEY=your_openai_key
OPENAI_ASSISTANT_ID=your_assistant_id
OPENAI_VECTOR_STORE_ID=your_vector_store_id
DADATA_API_KEY=your_dadata_key
DADATA_SECRET_KEY=your_dadata_secret
```

### 3. Создание Assistant

```bash
python setup.py create-assistant
```

Добавьте полученные ID в `.env`.

## Локальный запуск с Vercel Dev

### Установка Vercel CLI

```bash
npm install -g vercel
```

### Запуск dev сервера

```bash
vercel dev
```

Это запустит локальный сервер на `http://localhost:3000`.

### Настройка ngrok для webhook

Telegram требует HTTPS webhook. Используйте ngrok:

```bash
# Установите ngrok
brew install ngrok  # Mac
# или скачайте с https://ngrok.com/

# Запустите туннель
ngrok http 3000
```

Вы получите URL типа `https://abc123.ngrok.io`.

### Установка webhook

```bash
python setup.py set-webhook https://abc123.ngrok.io/api/webhook
```

Теперь бот будет получать обновления через локальный сервер!

## Тестирование без webhook (polling)

Для локальной разработки можно использовать polling вместо webhook.

Создайте `local_bot.py`:

```python
"""Local bot runner with polling instead of webhook."""
import asyncio
import logging
from telegram.ext import Application
from config import config
from api.webhook import get_application

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def main():
    """Run bot with polling."""
    # Validate config
    config.validate()
    
    # Get application (reuse webhook handlers)
    app = get_application()
    
    # Run with polling
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    print("Bot is running with polling...")
    print("Press Ctrl+C to stop")
    
    # Keep running
    await asyncio.Event().wait()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped")
```

Запуск:

```bash
python local_bot.py
```

## Отладка

### Включение debug логов

В `.env`:

```env
LOG_LEVEL=DEBUG
```

### Просмотр логов в реальном времени

```bash
# Vercel dev
vercel dev

# Логи будут в консоли

# Polling mode
python local_bot.py
```

### Тестирование отдельных компонентов

#### Тест DaData API

```python
from bot.services.mcp_dadata import mcp_dadata_service

# Тест поиска по ИНН
company = mcp_dadata_service.find_by_inn("7707083893")
print(company)
```

#### Тест Assistant

```python
from bot.services.assistant import assistant_service

# Тест форматирования
response = assistant_service.query_company(
    user_id=123,
    query="Покажи краткую информацию",
    company_data={"data": {"inn": "7707083893"}}
)
print(response)
```

#### Тест PDF экспорта

```python
from bot.services.pdf_export import pdf_service
from bot.services.mcp_dadata import mcp_dadata_service

# Получить данные
company = mcp_dadata_service.find_by_inn("7707083893")

# Сгенерировать PDF
pdf_buffer = pdf_service.export_full_report(company)

# Сохранить для проверки
with open("test_report.pdf", "wb") as f:
    f.write(pdf_buffer.getvalue())
```

## Unit тесты

Создайте `tests/test_services.py`:

```python
"""Unit tests for services."""
import unittest
from bot.services.mcp_dadata import mcp_dadata_service

class TestMCPDaData(unittest.TestCase):
    def test_find_by_inn_valid(self):
        """Test finding company by valid INN."""
        result = mcp_dadata_service.find_by_inn("7707083893")
        self.assertIsNotNone(result)
        self.assertEqual(result['data']['inn'], "7707083893")
    
    def test_find_by_inn_invalid(self):
        """Test finding company by invalid INN."""
        result = mcp_dadata_service.find_by_inn("0000000000")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
```

Запуск тестов:

```bash
python -m pytest tests/
```

## Проверка структуры проекта

```bash
# Проверить синтаксис всех Python файлов
find . -name "*.py" -exec python -m py_compile {} \;

# Проверить импорты
python -c "from api.webhook import handler; print('OK')"
```

## Мониторинг производительности

### Замер времени обработки

Добавьте в handlers:

```python
import time

start = time.time()
# ... your code ...
elapsed = time.time() - start
logger.info(f"Processing time: {elapsed:.2f}s")
```

### Отслеживание Vector Store

```python
from bot.services.assistant import assistant_service

# Проверить thread для пользователя
thread_id = assistant_service.get_or_create_thread(user_id)
print(f"Thread ID: {thread_id}")

# Проверить Vector Store
results = assistant_service.search_vector_store("query")
print(f"Found {len(results)} results")
```

## Отладка webhook

### Проверка доступности endpoint

```bash
curl -X GET https://your-url.vercel.app/api/webhook
```

Ответ должен быть:

```json
{
  "status": "ok",
  "message": "Telegram Bot Webhook is running"
}
```

### Тест POST запроса

```bash
curl -X POST https://your-url.vercel.app/api/webhook \
  -H "Content-Type: application/json" \
  -d '{"update_id": 1, "message": {"text": "/start"}}'
```

### Проверка webhook в Telegram

```bash
python setup.py webhook-info
```

## Частые проблемы и решения

### Проблема: "Module not found"

```bash
# Убедитесь, что установлены все зависимости
pip install -r requirements.txt

# Проверьте PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/project"
```

### Проблема: "OpenAI API Error"

```bash
# Проверьте ключ
python -c "from openai import OpenAI; client = OpenAI(); print('OK')"

# Проверьте Assistant ID
python -c "from config import config; print(config.OPENAI_ASSISTANT_ID)"
```

### Проблема: "DaData API Error"

```bash
# Проверьте ключи
python -c "from bot.services.mcp_dadata import mcp_dadata_service; \
           company = mcp_dadata_service.find_by_inn('7707083893'); \
           print('OK' if company else 'FAILED')"
```

### Проблема: Webhook не получает обновления

1. Проверьте URL webhook
2. Убедитесь, что используется HTTPS
3. Проверьте, что ngrok запущен
4. Переустановите webhook

```bash
python setup.py set-webhook https://your-new-url.vercel.app/api/webhook
```

## Профилирование

### Memory profiling

```bash
pip install memory_profiler

# Добавьте @profile декоратор к функциям
python -m memory_profiler your_script.py
```

### Time profiling

```bash
pip install line_profiler

# Добавьте @profile декоратор
kernprof -l -v your_script.py
```

## Развертывание изменений

### 1. Локальное тестирование

```bash
# Тест с vercel dev
vercel dev

# Или с polling
python local_bot.py
```

### 2. Preview deployment

```bash
# Создает preview URL
vercel

# Проверьте на preview URL
python setup.py set-webhook https://preview-url.vercel.app/api/webhook
```

### 3. Production deployment

```bash
# Деплой в production
vercel --prod

# Обновите webhook
python setup.py set-webhook https://your-app.vercel.app/api/webhook
```

## Best practices

1. **Всегда тестируйте локально** перед деплоем
2. **Используйте preview** для проверки изменений
3. **Проверяйте логи** после каждого деплоя
4. **Мониторьте использование** OpenAI API
5. **Кэшируйте часто** запрашиваемые данные
6. **Обрабатывайте ошибки** gracefully
7. **Логируйте важные** события
8. **Документируйте изменения** в коде

## Полезные команды

```bash
# Проверка версии Python
python --version

# Список установленных пакетов
pip list

# Обновление зависимостей
pip install --upgrade -r requirements.txt

# Проверка кода (flake8)
pip install flake8
flake8 bot/ api/

# Форматирование кода (black)
pip install black
black bot/ api/

# Type checking (mypy)
pip install mypy
mypy bot/ api/
```

## Ресурсы

- [Vercel CLI Documentation](https://vercel.com/docs/cli)
- [python-telegram-bot Documentation](https://docs.python-telegram-bot.org/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [DaData API Docs](https://dadata.ru/api/)
