"""Company screen handlers using OpenAI Assistant."""
import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.services.assistant import assistant_service
from bot.services.mcp_dadata import mcp_dadata_service
from bot.utils.keyboards import (
    get_company_menu_keyboard,
    get_back_keyboard,
    get_export_menu_keyboard,
    get_pagination_keyboard
)

logger = logging.getLogger(__name__)


async def show_company_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show main company info."""
    query = update.callback_query
    await query.answer()
    
    # Extract INN from callback data
    inn = query.data.split(':')[1] if ':' in query.data else context.user_data.get('inn')
    
    if not inn:
        await query.edit_message_text("❌ Ошибка: ИНН не найден")
        return
    
    # Get company data from MCP DaData
    company_data = mcp_dadata_service.find_by_inn(inn)
    
    if not company_data:
        await query.edit_message_text("❌ Компания не найдена")
        return
    
    # Store in context
    context.user_data['company'] = company_data
    context.user_data['inn'] = inn
    
    # Format using Assistant
    user_id = update.effective_user.id
    message = assistant_service.format_screen(user_id, 'brief', company_data)
    
    await query.edit_message_text(
        message,
        parse_mode='HTML',
        reply_markup=get_company_menu_keyboard(inn)
    )


async def show_finances_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show finances screen."""
    query = update.callback_query
    await query.answer()
    
    inn = query.data.split(':')[1] if ':' in query.data else context.user_data.get('inn')
    
    if not inn:
        await query.edit_message_text("❌ Ошибка: ИНН не найден")
        return
    
    # Get finance data from MCP
    finance_data = mcp_dadata_service.get_company_finances(inn)
    
    # Format using Assistant
    user_id = update.effective_user.id
    company_data = context.user_data.get('company') or mcp_dadata_service.find_by_inn(inn)
    
    if company_data:
        company_data['data']['finance'] = finance_data
    
    message = assistant_service.format_screen(user_id, 'finances', company_data)
    
    await query.edit_message_text(
        message,
        parse_mode='HTML',
        reply_markup=get_back_keyboard(f"company:{inn}")
    )


async def show_requisites_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show requisites screen."""
    query = update.callback_query
    await query.answer()
    
    inn = query.data.split(':')[1] if ':' in query.data else context.user_data.get('inn')
    company_data = context.user_data.get('company') or mcp_dadata_service.find_by_inn(inn)
    
    user_id = update.effective_user.id
    message = assistant_service.format_screen(user_id, 'requisites', company_data)
    
    await query.edit_message_text(
        message,
        parse_mode='HTML',
        reply_markup=get_back_keyboard(f"company:{inn}")
    )


async def show_address_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show address screen."""
    query = update.callback_query
    await query.answer()
    
    inn = query.data.split(':')[1] if ':' in query.data else context.user_data.get('inn')
    company_data = context.user_data.get('company') or mcp_dadata_service.find_by_inn(inn)
    
    user_id = update.effective_user.id
    message = assistant_service.format_screen(user_id, 'address', company_data)
    
    await query.edit_message_text(
        message,
        parse_mode='HTML',
        reply_markup=get_back_keyboard(f"company:{inn}")
    )


async def show_directors_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show directors history screen."""
    query = update.callback_query
    await query.answer()
    
    inn = query.data.split(':')[1] if ':' in query.data else context.user_data.get('inn')
    company_data = context.user_data.get('company') or mcp_dadata_service.find_by_inn(inn)
    
    user_id = update.effective_user.id
    message = assistant_service.format_screen(user_id, 'directors', company_data)
    
    await query.edit_message_text(
        message,
        parse_mode='HTML',
        reply_markup=get_back_keyboard(f"company:{inn}")
    )


async def show_founders_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show founders screen."""
    query = update.callback_query
    await query.answer()
    
    inn = query.data.split(':')[1] if ':' in query.data else context.user_data.get('inn')
    company_data = context.user_data.get('company') or mcp_dadata_service.find_by_inn(inn)
    
    user_id = update.effective_user.id
    message = assistant_service.format_screen(user_id, 'founders', company_data)
    
    await query.edit_message_text(
        message,
        parse_mode='HTML',
        reply_markup=get_back_keyboard(f"company:{inn}")
    )


async def show_addresses_history_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show addresses history screen."""
    query = update.callback_query
    await query.answer()
    
    inn = query.data.split(':')[1] if ':' in query.data else context.user_data.get('inn')
    company_data = context.user_data.get('company') or mcp_dadata_service.find_by_inn(inn)
    
    user_id = update.effective_user.id
    message = assistant_service.format_screen(user_id, 'addresses_history', company_data)
    
    await query.edit_message_text(
        message,
        parse_mode='HTML',
        reply_markup=get_back_keyboard(f"company:{inn}")
    )


async def show_okved_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show OKVED screen."""
    query = update.callback_query
    await query.answer()
    
    inn = query.data.split(':')[1] if ':' in query.data else context.user_data.get('inn')
    company_data = context.user_data.get('company') or mcp_dadata_service.find_by_inn(inn)
    
    user_id = update.effective_user.id
    message = assistant_service.format_screen(user_id, 'okved', company_data)
    
    await query.edit_message_text(
        message,
        parse_mode='HTML',
        reply_markup=get_back_keyboard(f"company:{inn}")
    )


async def show_history_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show history submenu."""
    query = update.callback_query
    await query.answer()
    
    inn = query.data.split(':')[1] if ':' in query.data else context.user_data.get('inn')
    
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    keyboard = [
        [InlineKeyboardButton("👤 Директора", callback_data=f"directors:{inn}")],
        [InlineKeyboardButton("👥 Учредители", callback_data=f"founders:{inn}")],
        [InlineKeyboardButton("📍 Адреса", callback_data=f"addresses_history:{inn}")],
        [InlineKeyboardButton("📊 ОКВЭД", callback_data=f"okved:{inn}")],
        [InlineKeyboardButton("◀️ Назад", callback_data=f"company:{inn}")],
    ]
    
    await query.edit_message_text(
        "📚 <b>История изменений</b>\n\nВыберите раздел:",
        parse_mode='HTML',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def show_export_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show export menu."""
    query = update.callback_query
    await query.answer()
    
    inn = query.data.split(':')[1] if ':' in query.data else context.user_data.get('inn')
    screen = query.data.split(':')[2] if len(query.data.split(':')) > 2 else 'main'
    
    await query.edit_message_text(
        "📄 <b>Экспорт в PDF</b>\n\nВыберите формат:",
        parse_mode='HTML',
        reply_markup=get_export_menu_keyboard(inn, screen)
    )
