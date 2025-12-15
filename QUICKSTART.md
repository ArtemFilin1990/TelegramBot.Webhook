# 🚀 Быстрый старт

Чек-лист для развертывания Telegram-бота на Vercel за 10 минут.

## ✅ Предварительные требования

- [ ] Аккаунт на [Vercel](https://vercel.com)
- [ ] Python 3.11 установлен
- [ ] Git установлен
- [ ] Node.js установлен (для Vercel CLI)

## 📋 Шаг за шагом

### 1️⃣ Получите API ключи (5 мин)

- [ ] **Telegram Bot Token**
  - Откройте [@BotFather](https://t.me/BotFather) в Telegram
  - `/newbot` → следуйте инструкциям
  - Скопируйте токен

- [ ] **OpenAI API Key**
  - Зарегистрируйтесь на [platform.openai.com](https://platform.openai.com)
  - API Keys → Create new key
  - Скопируйте ключ

- [ ] **DaData Keys**
  - Зарегистрируйтесь на [dadata.ru](https://dadata.ru)
  - Личный кабинет → API ключи
  - Скопируйте API key и Secret key

### 2️⃣ Клонируйте и настройте (2 мин)

```bash
# Клонируйте репозиторий
git clone https://github.com/ArtemFilin1990/TelegramBot.Webhook.git
cd TelegramBot.Webhook

# Установите зависимости
pip install -r requirements.txt

# Создайте .env
cp .env.example .env
```

**Заполните .env:**
```env
TELEGRAM_BOT_TOKEN=<ваш_токен_из_BotFather>
OPENAI_API_KEY=<ваш_openai_ключ>
DADATA_API_KEY=<ваш_dadata_api_key>
DADATA_SECRET_KEY=<ваш_dadata_secret_key>
```

### 3️⃣ Создайте OpenAI Assistant (1 мин)

```bash
python setup.py create-assistant
```

Добавьте полученные ID в `.env`:
```env
OPENAI_ASSISTANT_ID=asst_xxxxx
OPENAI_VECTOR_STORE_ID=vs_xxxxx
```

### 4️⃣ Деплой на Vercel (2 мин)

```bash
# Установите Vercel CLI
npm i -g vercel

# Логин
vercel login

# Деплой
vercel
```

Следуйте подсказкам:
- Project name: `telegram-egrul-bot` (или свое название)
- Deploy: `Yes`

Vercel выдаст URL: `https://your-app.vercel.app`

### 5️⃣ Настройте переменные окружения в Vercel (3 мин)

```bash
vercel env add TELEGRAM_BOT_TOKEN
# Вставьте токен, Enter
# Выберите: Production, Preview, Development

vercel env add OPENAI_API_KEY
vercel env add OPENAI_ASSISTANT_ID
vercel env add OPENAI_VECTOR_STORE_ID
vercel env add DADATA_API_KEY
vercel env add DADATA_SECRET_KEY
```

Повторный деплой с переменными:
```bash
vercel --prod
```

### 6️⃣ Установите webhook (1 мин)

```bash
python setup.py set-webhook https://your-app.vercel.app/api/webhook
```

Должно вывести:
```
✅ Webhook set successfully
```

### 7️⃣ Тестируйте! (1 мин)

1. Откройте Telegram
2. Найдите вашего бота
3. `/start`
4. Попробуйте поиск: `7707083893` (ИНН Сбербанка)

## 🎉 Готово!

Ваш бот работает на Vercel и готов к использованию!

## 🔍 Проверка

### Проверить webhook
```bash
python setup.py webhook-info
```

### Посмотреть логи
```bash
vercel logs
```

Или в [Vercel Dashboard](https://vercel.com/dashboard) → Ваш проект → Logs

## 📚 Дополнительно

- [README.md](README.md) - Полная документация
- [DEPLOYMENT.md](DEPLOYMENT.md) - Детальное руководство по деплою
- [ARCHITECTURE.md](ARCHITECTURE.md) - Архитектура системы
- [DEVELOPMENT.md](DEVELOPMENT.md) - Локальная разработка
- [EXAMPLES.md](EXAMPLES.md) - Примеры использования

## 🆘 Проблемы?

### Бот не отвечает
1. Проверьте логи: `vercel logs`
2. Проверьте webhook: `python setup.py webhook-info`
3. Переустановите webhook

### Ошибки в логах
- Проверьте переменные: `vercel env ls`
- Убедитесь, что все ключи корректны
- Проверьте баланс OpenAI API

### DaData не работает
- Проверьте ключи в личном кабинете dadata.ru
- Убедитесь, что API включен

## 💡 Совет

Для разработки используйте локальный режим:

```bash
# Установите ngrok
brew install ngrok  # Mac

# Запустите Vercel dev
vercel dev

# В другом терминале
ngrok http 3000

# Установите webhook на ngrok URL
python setup.py set-webhook https://xxxxx.ngrok.io/api/webhook
```

## 📊 Стоимость

### Бесплатный тариф (достаточно для старта):
- **Vercel**: Free tier (до 100 GB трафика)
- **OpenAI**: Pay-as-you-go (~$0.01-0.03 за запрос)
- **DaData**: Бесплатный тариф (ограниченные данные)

### Рекомендуется:
- **DaData**: Платный тариф от 1000₽/мес для полных данных
- **OpenAI**: Пополните баланс $10-20 для начала
- **Vercel**: Free tier обычно достаточно

## 🎯 Что дальше?

1. Протестируйте все функции
2. Настройте собственный домен (опционально)
3. Мониторьте использование API
4. Расширяйте функционал по необходимости

---

**Нужна помощь?** Откройте Issue в GitHub: [github.com/ArtemFilin1990/TelegramBot.Webhook/issues](https://github.com/ArtemFilin1990/TelegramBot.Webhook/issues)
