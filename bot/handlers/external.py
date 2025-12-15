"""External modules handlers: courts and procurement."""
import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.services.court import court_service
from bot.services.procurement import procurement_service
from bot.services.mcp_dadata import mcp_dadata_service
from bot.utils.keyboards import get_pagination_keyboard, get_back_keyboard

logger = logging.getLogger(__name__)


async def show_court_cases_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show court cases screen."""
    query = update.callback_query
    await query.answer()
    
    parts = query.data.split(':')
    inn = parts[1] if len(parts) > 1 else context.user_data.get('inn')
    page = int(parts[2]) if len(parts) > 2 else 1
    
    if not inn:
        await query.edit_message_text("❌ Ошибка: ИНН не найден")
        return
    
    # Get company data for context
    company_data = context.user_data.get('company') or mcp_dadata_service.find_by_inn(inn)
    company_name = company_data.get('data', {}).get('name', {}).get('short', 'Компания') if company_data else 'Компания'
    
    # Get court cases (best-effort parsing)
    await query.edit_message_text("⏳ Поиск судебных дел...")
    
    cases_data = court_service.search_cases(inn=inn, company_name=company_name, page=page)
    
    message = f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ⚖️ СУДЕБНЫЕ ДЕЛА
┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛

<b>Компания:</b> {company_name}
<b>ИНН:</b> <code>{inn}</code>

"""
    
    cases = cases_data.get('cases', [])
    total = cases_data.get('total', 0)
    note = cases_data.get('note', '')
    
    if not cases:
        message += f"ℹ️ Дела не найдены\n\n<i>{note}</i>"
    else:
        message += f"<b>Всего дел:</b> {total}\n<b>Страница:</b> {page}\n\n"
        for i, case in enumerate(cases, 1):
            case_num = case.get('number', 'Н/Д')
            case_date = case.get('date', 'Н/Д')
            case_status = case.get('status', 'Н/Д')
            message += f"{i}. <b>{case_num}</b>\n"
            message += f"   📅 {case_date}\n"
            message += f"   📊 {case_status}\n\n"
        
        if note:
            message += f"\n<i>{note}</i>"
    
    # Pagination
    per_page = cases_data.get('per_page', 10)
    total_pages = max(1, (total + per_page - 1) // per_page)
    
    if total_pages > 1:
        keyboard = get_pagination_keyboard(page, total_pages, 'court', inn)
    else:
        keyboard = get_back_keyboard(f"company:{inn}")
    
    await query.edit_message_text(
        message,
        parse_mode='HTML',
        reply_markup=keyboard
    )


async def show_procurement_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show government procurement screen."""
    query = update.callback_query
    await query.answer()
    
    parts = query.data.split(':')
    inn = parts[1] if len(parts) > 1 else context.user_data.get('inn')
    page = int(parts[2]) if len(parts) > 2 else 1
    
    if not inn:
        await query.edit_message_text("❌ Ошибка: ИНН не найден")
        return
    
    # Get company data for context
    company_data = context.user_data.get('company') or mcp_dadata_service.find_by_inn(inn)
    company_name = company_data.get('data', {}).get('name', {}).get('short', 'Компания') if company_data else 'Компания'
    
    # Get procurement data (best-effort parsing)
    await query.edit_message_text("⏳ Поиск госзакупок...")
    
    procurement_data = procurement_service.search_procurements(inn=inn, company_name=company_name, page=page)
    
    message = f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 🏛 ГОСЗАКУПКИ
┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛

<b>Компания:</b> {company_name}
<b>ИНН:</b> <code>{inn}</code>

"""
    
    procurements = procurement_data.get('procurements', [])
    total = procurement_data.get('total', 0)
    note = procurement_data.get('note', '')
    
    if not procurements:
        message += f"ℹ️ Закупки не найдены\n\n<i>{note}</i>"
    else:
        message += f"<b>Всего закупок:</b> {total}\n<b>Страница:</b> {page}\n\n"
        for i, proc in enumerate(procurements, 1):
            proc_num = proc.get('number', 'Н/Д')
            proc_date = proc.get('date', 'Н/Д')
            proc_sum = proc.get('sum', 'Н/Д')
            proc_status = proc.get('status', 'Н/Д')
            message += f"{i}. <b>{proc_num}</b>\n"
            message += f"   📅 {proc_date}\n"
            message += f"   💰 {proc_sum}\n"
            message += f"   📊 {proc_status}\n\n"
        
        if note:
            message += f"\n<i>{note}</i>"
    
    # Pagination
    per_page = procurement_data.get('per_page', 10)
    total_pages = max(1, (total + per_page - 1) // per_page)
    
    if total_pages > 1:
        keyboard = get_pagination_keyboard(page, total_pages, 'procurement', inn)
    else:
        keyboard = get_back_keyboard(f"company:{inn}")
    
    await query.edit_message_text(
        message,
        parse_mode='HTML',
        reply_markup=keyboard
    )


async def handle_pagination(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle pagination for courts and procurement."""
    query = update.callback_query
    await query.answer()
    
    # Parse callback data: prefix:action:current_page:inn
    parts = query.data.split(':')
    prefix = parts[0]
    action = parts[1]
    current_page = int(parts[2])
    inn = parts[3] if len(parts) > 3 else context.user_data.get('inn')
    
    # Calculate new page
    new_page = current_page + 1 if action == 'next' else current_page - 1
    
    # Route to appropriate handler
    if prefix == 'court':
        context.user_data['temp_callback'] = f"court:{inn}:{new_page}"
        await show_court_cases_callback(update, context)
    elif prefix == 'procurement':
        context.user_data['temp_callback'] = f"procurement:{inn}:{new_page}"
        await show_procurement_callback(update, context)
