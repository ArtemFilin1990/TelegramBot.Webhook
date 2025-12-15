"""Main bot handlers."""
import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.keyboards import get_main_menu_keyboard
from bot.utils.formatters import format_help

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    user = update.effective_user
    
    welcome_message = f"""
👋 Привет, {user.first_name}!

Я бот для поиска информации о российских компаниях.

Могу найти данные по ИНН или ОГРН:
• Основная информация
• Руководители и учредители
• Адреса и ОКВЭД
• Судебные дела
• Госзакупки
• Экспорт в PDF

Выберите действие:
"""
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=get_main_menu_keyboard()
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    help_text = format_help()
    await update.message.reply_text(help_text, parse_mode='HTML')


async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle main menu callback."""
    query = update.callback_query
    await query.answer()
    
    welcome_message = """
🏠 <b>Главное меню</b>

Выберите действие:
"""
    
    await query.edit_message_text(
        welcome_message,
        reply_markup=get_main_menu_keyboard(),
        parse_mode='HTML'
    )


async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle help callback."""
    query = update.callback_query
    await query.answer()
    
    help_text = format_help()
    await query.edit_message_text(help_text, parse_mode='HTML', reply_markup=get_main_menu_keyboard())
