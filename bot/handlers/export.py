"""Export handlers for PDF generation."""
import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.services.pdf_export import pdf_service
from bot.services.mcp_dadata import mcp_dadata_service
from bot.utils.keyboards import get_back_keyboard

logger = logging.getLogger(__name__)


async def export_screen_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Export current screen to PDF."""
    query = update.callback_query
    await query.answer("📄 Генерация PDF...")
    
    parts = query.data.split(':')
    inn = parts[1] if len(parts) > 1 else context.user_data.get('inn')
    screen = parts[2] if len(parts) > 2 else 'main'
    
    if not inn:
        await query.edit_message_text("❌ Ошибка: ИНН не найден")
        return
    
    # Get company data
    company_data = context.user_data.get('company') or mcp_dadata_service.find_by_inn(inn)
    
    if not company_data:
        await query.edit_message_text("❌ Данные компании не найдены")
        return
    
    try:
        # Generate PDF
        screen_names = {
            'main': 'Основная информация',
            'finances': 'Финансы',
            'requisites': 'Реквизиты',
            'address': 'Адрес',
            'directors': 'Директора',
            'founders': 'Учредители',
            'addresses_history': 'История адресов',
            'okved': 'ОКВЭД'
        }
        
        screen_name = screen_names.get(screen, 'Отчет')
        pdf_buffer = pdf_service.export_company_screen(company_data, screen_name)
        
        company_name = company_data.get('data', {}).get('name', {}).get('short', 'company')
        filename = f"{company_name}_{screen}.pdf"
        
        # Send PDF
        await query.message.reply_document(
            document=pdf_buffer,
            filename=filename,
            caption=f"📄 Экспорт: {screen_name}"
        )
        
        await query.edit_message_text(
            "✅ PDF успешно сгенерирован",
            reply_markup=get_back_keyboard(f"company:{inn}")
        )
        
    except Exception as e:
        logger.error(f"Error generating PDF: {e}")
        await query.edit_message_text(
            f"❌ Ошибка при генерации PDF: {str(e)}",
            reply_markup=get_back_keyboard(f"company:{inn}")
        )


async def export_full_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Export full company report to PDF."""
    query = update.callback_query
    await query.answer("📚 Генерация полного отчёта...")
    
    inn = query.data.split(':')[1] if ':' in query.data else context.user_data.get('inn')
    
    if not inn:
        await query.edit_message_text("❌ Ошибка: ИНН не найден")
        return
    
    # Get company data
    company_data = context.user_data.get('company') or mcp_dadata_service.find_by_inn(inn)
    
    if not company_data:
        await query.edit_message_text("❌ Данные компании не найдены")
        return
    
    try:
        # Generate full PDF report
        pdf_buffer = pdf_service.export_full_report(company_data)
        
        company_name = company_data.get('data', {}).get('name', {}).get('short', 'company')
        filename = f"{company_name}_full_report.pdf"
        
        # Send PDF
        await query.message.reply_document(
            document=pdf_buffer,
            filename=filename,
            caption="📚 Полный отчёт по компании"
        )
        
        await query.edit_message_text(
            "✅ Полный отчёт успешно сгенерирован",
            reply_markup=get_back_keyboard(f"company:{inn}")
        )
        
    except Exception as e:
        logger.error(f"Error generating full report: {e}")
        await query.edit_message_text(
            f"❌ Ошибка при генерации отчёта: {str(e)}",
            reply_markup=get_back_keyboard(f"company:{inn}")
        )
