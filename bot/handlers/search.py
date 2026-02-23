"""Search handlers for INN/OGRN lookup."""
import logging
import re
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from bot.services.dadata import dadata_service
from bot.utils.keyboards import get_company_menu_keyboard, get_main_menu_keyboard
from bot.utils.formatters import format_company_info
from db import create_pool, init_db, log_request

logger = logging.getLogger(__name__)
db_pool = None

# Conversation states
AWAITING_INN, AWAITING_OGRN = range(2)


async def search_inn_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle search by INN callback."""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "🔍 <b>Поиск по ИНН</b>\n\n"
        "Введите ИНН компании (10 или 12 цифр):",
        parse_mode='HTML'
    )
    
    context.user_data['state'] = 'awaiting_inn'
    return AWAITING_INN


async def search_ogrn_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle search by OGRN callback."""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "🏢 <b>Поиск по ОГРН</b>\n\n"
        "Введите ОГРН компании (13 или 15 цифр):",
        parse_mode='HTML'
    )
    
    context.user_data['state'] = 'awaiting_ogrn'
    return AWAITING_OGRN


async def handle_inn_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle INN input from user."""
    inn = update.message.text.strip()
    
    # Validate INN format
    if not re.match(r'^\d{10}$|^\d{12}$', inn):
        await update.message.reply_text(
            "❌ Неверный формат ИНН.\n"
            "ИНН должен содержать 10 или 12 цифр.\n\n"
            "Попробуйте еще раз:",
            parse_mode='HTML'
        )
        return AWAITING_INN
    
    # Show loading message
    loading_msg = await update.message.reply_text("⏳ Поиск информации...")
    
    # Search company
       global db_pool
    if db_pool is None:
        db_pool = await create_pool()
        await init_db(db_pool)
    await log_request(db_pool, inn)

    company_data = dadata_service.find_by_inn(inn)
    
    if not company_data:
        await loading_msg.edit_text(
            "❌ Компания с таким ИНН не найдена.\n\n"
   #  # gobal db_pool
    i###f db_pool is None:
     #   db_pool = await create_pool()
     #   await init_db(db_pool)
   # a#wait log_request(db_pool, inn)

            "Попробуйте другой ИНН:",
            parse_mode='HTML'
        )
        return AWAITING_INN
    
    # Store company data
    context.user_data['company'] = company_data
    context.user_data['inn'] = inn
    
    # Format and send company info
    message = format_company_info(company_data)
    await loading_msg.edit_text(
        message,
        parse_mode='HTML',
        reply_markup=get_company_menu_keyboard(inn)
    )
    
    context.user_data['state'] = None
    return ConversationHandler.END


async def handle_ogrn_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle OGRN input from user."""
    ogrn = update.message.text.strip()
    
    # Validate OGRN format
    if not re.match(r'^\d{13}$|^\d{15}$', ogrn):
        await update.message.reply_text(
            "❌ Неверный формат ОГРН.\n"
            "ОГРН должен содержать 13 или 15 цифр.\n\n"
            "Попробуйте еще раз:",
            parse_mode='HTML'
        )
        return AWAITING_OGRN
    
    # Show loading message
    loading_msg = await update.message.reply_text("⏳ Поиск информации...")
    
    # Search company
    company_data = dadata_service.find_by_ogrn(ogrn)
    
    if not company_data:
        await loading_msg.edit_text(
            "❌ Компания с таким ОГРН не найдена.\n\n"
            "Попробуйте другой ОГРН:",
            parse_mode='HTML'
        )
        return AWAITING_OGRN
    
    # Store company data
    context.user_data['company'] = company_data
    inn = company_data.get('data', {}).get('inn', '')
    context.user_data['inn'] = inn
    
    # Format and send company info
    message = format_company_info(company_data)
    await loading_msg.edit_text(
        message,
        parse_mode='HTML',
        reply_markup=get_company_menu_keyboard(inn)
    )
    
    context.user_data['state'] = None
    return ConversationHandler.END


async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle conversation cancellation."""
    context.user_data['state'] = None
    
    if update.message:
        await update.message.reply_text(
            "❌ Операция отменена.",
            reply_markup=get_main_menu_keyboard()
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            "❌ Операция отменена.",
            reply_markup=get_main_menu_keyboard()
        )
    
    return ConversationHandler.END
