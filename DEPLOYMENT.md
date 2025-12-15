# Руководство по развертыванию на Vercel

## Предварительные требования

1. Аккаунт на [Vercel](https://vercel.com)
2. [Vercel CLI](https://vercel.com/cli) установлен глобально
3. Python 3.11
4. Git

## Шаг 1: Получение API ключей

### Telegram Bot Token

1. Откройте Telegram и найдите [@BotFather](https://t.me/BotFather)
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен

### OpenAI API Key

1. Зарегистрируйтесь на [OpenAI Platform](https://platform.openai.com)
2. Перейдите в раздел [API Keys](https://platform.openai.com/api-keys)
3. Создайте новый ключ
4. Скопируйте ключ (он больше не будет показан)

### DaData API Keys

1. Зарегистрируйтесь на [DaData](https://dadata.ru)
2. Войдите в [личный кабинет](https://dadata.ru/profile/)
3. Скопируйте API ключ и Secret ключ

**Примечание:** Для доступа ко всем данным рекомендуется платный тариф DaData.

## Шаг 2: Настройка локального окружения

```bash
# Клонируйте репозиторий
git clone https://github.com/ArtemFilin1990/TelegramBot.Webhook.git
cd TelegramBot.Webhook

# Создайте виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установите зависимости
pip install -r requirements.txt

# Скопируйте .env.example в .env
cp .env.example .env
```

## Шаг 3: Создание OpenAI Assistant

```bash
# Заполните в .env ключи:
# TELEGRAM_BOT_TOKEN
# OPENAI_API_KEY
# DADATA_API_KEY
# DADATA_SECRET_KEY

# Создайте Assistant и Vector Store
python setup.py create-assistant
```

Скрипт выведет ID Assistant и Vector Store. Добавьте их в `.env`:

```env
OPENAI_ASSISTANT_ID=asst_xxxxxxxxxxxxx
OPENAI_VECTOR_STORE_ID=vs_xxxxxxxxxxxxx
```

## Шаг 4: Деплой на Vercel

### 4.1 Установка Vercel CLI

```bash
npm install -g vercel
```

### 4.2 Логин в Vercel

```bash
vercel login
```

### 4.3 Первый деплой

```bash
vercel
```

При первом запуске Vercel задаст вопросы:

```
? Set up and deploy "~/TelegramBot.Webhook"? [Y/n] y
? Which scope do you want to deploy to? <your-username>
? Link to existing project? [y/N] n
? What's your project's name? telegram-egrul-bot
? In which directory is your code located? ./
```

Vercel автоматически определит Python и настроит проект.

### 4.4 Настройка переменных окружения

После успешного деплоя, добавьте переменные окружения:

```bash
# Telegram
vercel env add TELEGRAM_BOT_TOKEN
# Вставьте токен, нажмите Enter

# OpenAI
vercel env add OPENAI_API_KEY
vercel env add OPENAI_ASSISTANT_ID
vercel env add OPENAI_VECTOR_STORE_ID

# DaData
vercel env add DADATA_API_KEY
vercel env add DADATA_SECRET_KEY
```

Для каждой переменной выберите окружения:
```
? What's the value of TELEGRAM_BOT_TOKEN? <paste-your-token>
? Add TELEGRAM_BOT_TOKEN to which Environments? Production, Preview, Development
```

### 4.5 Повторный деплой с переменными

```bash
vercel --prod
```

После деплоя вы получите URL вашего приложения, например:
```
https://telegram-egrul-bot.vercel.app
```

## Шаг 5: Настройка Telegram Webhook

```bash
# Используйте полученный URL
python setup.py set-webhook https://telegram-egrul-bot.vercel.app/api/webhook
```

Должно вывести:
```
✅ Webhook set successfully
URL: https://telegram-egrul-bot.vercel.app/api/webhook
```

### Проверка webhook

```bash
python setup.py webhook-info
```

Вывод должен показать:
```
Current webhook URL: https://telegram-egrul-bot.vercel.app/api/webhook
Pending updates: 0
```

## Шаг 6: Тестирование

1. Откройте Telegram
2. Найдите вашего бота по имени
3. Отправьте `/start`
4. Попробуйте поиск по ИНН или ОГРН

## Просмотр логов

### В Vercel Dashboard

1. Откройте [Vercel Dashboard](https://vercel.com/dashboard)
2. Выберите ваш проект
3. Перейдите в раздел "Logs"
4. Фильтруйте по функции `api/webhook`

### Через CLI

```bash
vercel logs
```

## Обновление кода

После изменений в коде:

```bash
git add .
git commit -m "Update: ваше описание"
git push

# Vercel автоматически задеплоит изменения
# Или задеплойте вручную:
vercel --prod
```

## Управление проектом в Vercel

### Настройки проекта

1. Откройте [Vercel Dashboard](https://vercel.com/dashboard)
2. Выберите проект
3. Перейдите в "Settings"

### Переменные окружения

Settings → Environment Variables

Здесь можно:
- Добавить новые переменные
- Изменить существующие
- Удалить ненужные

### Домены

Settings → Domains

Можно добавить собственный домен:
1. Добавьте домен
2. Настройте DNS записи
3. Подождите верификации

## Решение проблем

### Бот не отвечает

1. Проверьте логи в Vercel
2. Проверьте webhook:
   ```bash
   python setup.py webhook-info
   ```
3. Переустановите webhook:
   ```bash
   python setup.py set-webhook https://your-url.vercel.app/api/webhook
   ```

### Ошибки в логах

```bash
# Просмотрите логи
vercel logs

# Проверьте переменные окружения
vercel env ls
```

### Assistant не работает

1. Проверьте OPENAI_API_KEY
2. Проверьте OPENAI_ASSISTANT_ID
3. Пересоздайте Assistant:
   ```bash
   python setup.py create-assistant
   ```

### DaData не возвращает данные

1. Проверьте API ключи
2. Убедитесь, что у вас есть доступ к API
3. Проверьте баланс на dadata.ru

## Мониторинг

### Vercel Analytics

Vercel автоматически собирает метрики:
- Количество запросов
- Время выполнения
- Ошибки

Доступны в разделе "Analytics" проекта.

### Telegram Bot API

Проверка статуса бота:
```bash
curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe
```

## Безопасность

### Защита переменных окружения

- Никогда не коммитьте `.env` файл
- Используйте Vercel Environment Variables
- Регулярно обновляйте ключи

### HTTPS

Vercel автоматически предоставляет HTTPS для всех деплойментов.

## Стоимость

### Vercel

- Free tier: Достаточно для большинства ботов
- Pro tier ($20/мес): Больше лимитов и функций

### OpenAI

- Оплата за токены
- Примерная стоимость: $0.01-0.03 на запрос (зависит от модели)

### DaData

- Бесплатный тариф: Ограниченный доступ
- Платные тарифы: От 1000₽/мес

## Масштабирование

Vercel автоматически масштабирует ваше приложение:
- Автоматическое масштабирование функций
- CDN для статических ресурсов
- Глобальная инфраструктура

## Дополнительные ресурсы

- [Vercel Documentation](https://vercel.com/docs)
- [Python on Vercel](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [DaData API](https://dadata.ru/api/)
