"""iOS-style keyboard utilities for Telegram bot."""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_menu_keyboard():
    """Get main menu keyboard (iOS-style)."""
    keyboard = [
        [InlineKeyboardButton("🔍 Поиск по ИНН", callback_data="search_inn")],
        [InlineKeyboardButton("🏢 Поиск по ОГРН", callback_data="search_ogrn")],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data="help")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_company_menu_keyboard(inn: str):
    """Get company details menu keyboard (iOS-style)."""
    keyboard = [
        [InlineKeyboardButton("📊 Краткий отчёт", callback_data=f"brief:{inn}")],
        [InlineKeyboardButton("💰 Финансы", callback_data=f"finances:{inn}")],
        [InlineKeyboardButton("📋 Реквизиты", callback_data=f"requisites:{inn}")],
        [InlineKeyboardButton("📍 Адрес", callback_data=f"address:{inn}")],
        [InlineKeyboardButton("📚 История", callback_data=f"history:{inn}")],
        [InlineKeyboardButton("⚖️ Судебные дела", callback_data=f"court:{inn}")],
        [InlineKeyboardButton("🏛 Госзакупки", callback_data=f"procurement:{inn}")],
        [InlineKeyboardButton("📄 Экспорт PDF", callback_data=f"export_menu:{inn}")],
        [InlineKeyboardButton("◀️ Главное меню", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_export_menu_keyboard(inn: str, screen: str = "main"):
    """Get export menu keyboard."""
    keyboard = [
        [InlineKeyboardButton("📱 Экспорт текущего экрана", callback_data=f"export_screen:{inn}:{screen}")],
        [InlineKeyboardButton("📚 Полный отчет", callback_data=f"export_full:{inn}")],
        [InlineKeyboardButton("◀️ Назад", callback_data=f"company:{inn}")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_back_keyboard(callback_data: str):
    """Get back button keyboard."""
    keyboard = [
        [InlineKeyboardButton("◀️ Назад", callback_data=callback_data)]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_pagination_keyboard(current_page: int, total_pages: int, prefix: str, data: str = ""):
    """Get pagination keyboard (iOS-style)."""
    keyboard = []
    
    nav_buttons = []
    if current_page > 1:
        nav_buttons.append(InlineKeyboardButton("◀️", callback_data=f"{prefix}:prev:{current_page}:{data}"))
    
    nav_buttons.append(InlineKeyboardButton(f"• {current_page}/{total_pages} •", callback_data="noop"))
    
    if current_page < total_pages:
        nav_buttons.append(InlineKeyboardButton("▶️", callback_data=f"{prefix}:next:{current_page}:{data}"))
    
    keyboard.append(nav_buttons)
    keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data=f"company:{data}")])
    
    return InlineKeyboardMarkup(keyboard)


def get_confirmation_keyboard(confirm_action: str, cancel_action: str = "main_menu"):
    """Get confirmation keyboard."""
    keyboard = [
        [
            InlineKeyboardButton("✅ Да", callback_data=confirm_action),
            InlineKeyboardButton("❌ Нет", callback_data=cancel_action)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
