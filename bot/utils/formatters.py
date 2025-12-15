"""Message formatting utilities for iOS-style display."""
from typing import Dict, Any, List


def format_company_info(company_data: Dict[str, Any]) -> str:
    """Format company information in iOS style."""
    if not company_data:
        return "❌ Компания не найдена"
    
    data = company_data.get('data', {})
    
    # Company name
    name = data.get('name', {})
    full_name = name.get('full_with_opf', 'Н/Д')
    short_name = name.get('short_with_opf', '')
    
    # Basic info
    inn = data.get('inn', 'Н/Д')
    ogrn = data.get('ogrn', 'Н/Д')
    kpp = data.get('kpp', 'Н/Д')
    
    # Status
    state = data.get('state', {})
    status = state.get('status', 'Н/Д')
    reg_date = state.get('registration_date', 'Н/Д')
    
    # Management
    management = data.get('management', {})
    director = management.get('name', 'Н/Д')
    director_post = management.get('post', 'Руководитель')
    
    # Address
    address = data.get('address', {})
    addr_value = address.get('value', 'Н/Д')
    
    # Capital
    capital = data.get('capital', {})
    capital_value = capital.get('value', 'Н/Д') if capital else 'Н/Д'
    
    message = f"""
╔══════════════════════════════╗
    📊 ИНФОРМАЦИЯ О КОМПАНИИ
╚══════════════════════════════╝

🏢 <b>{full_name}</b>
{f'({short_name})' if short_name and short_name != full_name else ''}

┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 📋 РЕКВИЗИТЫ
┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛

• ИНН: <code>{inn}</code>
• ОГРН: <code>{ogrn}</code>
• КПП: <code>{kpp}</code>
• Статус: {status}
• Дата регистрации: {reg_date}

┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 👤 РУКОВОДСТВО
┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛

• {director_post}: {director}

┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 📍 АДРЕС
┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛

{addr_value}

┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 💰 УСТАВНЫЙ КАПИТАЛ
┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛

{capital_value}
"""
    
    return message.strip()


def format_directors(company_data: Dict[str, Any]) -> str:
    """Format directors information."""
    data = company_data.get('data', {})
    management = data.get('management', {})
    
    if not management:
        return "❌ Информация о руководителях отсутствует"
    
    name = management.get('name', 'Н/Д')
    post = management.get('post', 'Н/Д')
    
    message = f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 👤 ДИРЕКТОРА
┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛

<b>Текущий руководитель:</b>

• ФИО: {name}
• Должность: {post}

<i>Примечание: История изменений руководителей требует расширенной подписки DaData</i>
"""
    
    return message.strip()


def format_founders(company_data: Dict[str, Any]) -> str:
    """Format founders information."""
    data = company_data.get('data', {})
    founders = data.get('founders', [])
    
    if not founders:
        return "❌ Информация об учредителях отсутствует"
    
    message = """
┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 👥 УЧРЕДИТЕЛИ
┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛

"""
    
    for i, founder in enumerate(founders, 1):
        name = founder.get('name', 'Н/Д')
        share = founder.get('share', {})
        
        message += f"\n<b>{i}. {name}</b>\n"
        if share:
            message += f"   Доля: {share}\n"
    
    return message.strip()


def format_addresses(company_data: Dict[str, Any]) -> str:
    """Format addresses information."""
    data = company_data.get('data', {})
    address = data.get('address', {})
    
    if not address:
        return "❌ Информация об адресах отсутствует"
    
    addr_value = address.get('value', 'Н/Д')
    addr_data = address.get('data', {})
    
    message = f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 📍 АДРЕСА
┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛

<b>Юридический адрес:</b>
{addr_value}
"""
    
    if addr_data:
        postal = addr_data.get('postal_code', '')
        if postal:
            message += f"\n<b>Индекс:</b> {postal}"
    
    return message.strip()


def format_okved(company_data: Dict[str, Any]) -> str:
    """Format OKVED information."""
    data = company_data.get('data', {})
    okved = data.get('okved', '')
    okveds = data.get('okveds', [])
    
    if not okved and not okveds:
        return "❌ Информация об ОКВЭД отсутствует"
    
    message = f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 📊 ОКВЭД
┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛

<b>Основной вид деятельности:</b>
{okved}
"""
    
    if okveds:
        message += "\n\n<b>Дополнительные виды деятельности:</b>\n"
        for i, okv in enumerate(okveds[:10], 1):  # Limit to 10
            message += f"\n{i}. {okv}"
        
        if len(okveds) > 10:
            message += f"\n\n<i>... и еще {len(okveds) - 10} видов деятельности</i>"
    
    return message.strip()


def format_court_cases(cases_data: Dict[str, Any], page: int = 1) -> str:
    """Format court cases information."""
    cases = cases_data.get('cases', [])
    total = cases_data.get('total', 0)
    note = cases_data.get('note', '')
    
    message = """
┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ⚖️ СУДЕБНЫЕ ДЕЛА
┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛

"""
    
    if not cases:
        message += f"ℹ️ Дела не найдены\n\n<i>{note}</i>"
    else:
        message += f"<b>Всего дел:</b> {total}\n\n"
        for i, case in enumerate(cases, 1):
            case_num = case.get('number', 'Н/Д')
            case_date = case.get('date', 'Н/Д')
            case_status = case.get('status', 'Н/Д')
            message += f"{i}. {case_num}\n   Дата: {case_date}\n   Статус: {case_status}\n\n"
    
    return message.strip()


def format_procurements(procurements_data: Dict[str, Any], page: int = 1) -> str:
    """Format government procurements information."""
    procurements = procurements_data.get('procurements', [])
    total = procurements_data.get('total', 0)
    note = procurements_data.get('note', '')
    
    message = """
┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 🏛 ГОСЗАКУПКИ
┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛

"""
    
    if not procurements:
        message += f"ℹ️ Закупки не найдены\n\n<i>{note}</i>"
    else:
        message += f"<b>Всего закупок:</b> {total}\n\n"
        for i, proc in enumerate(procurements, 1):
            proc_num = proc.get('number', 'Н/Д')
            proc_date = proc.get('date', 'Н/Д')
            proc_sum = proc.get('sum', 'Н/Д')
            message += f"{i}. {proc_num}\n   Дата: {proc_date}\n   Сумма: {proc_sum}\n\n"
    
    return message.strip()


def format_help() -> str:
    """Format help message."""
    return """
╔══════════════════════════════╗
    ℹ️ ПОМОЩЬ
╚══════════════════════════════╝

<b>Доступные команды:</b>

🔍 <b>Поиск по ИНН</b>
Введите 10 или 12-значный ИНН компании

🏢 <b>Поиск по ОГРН</b>
Введите 13 или 15-значный ОГРН компании

<b>Функции бота:</b>

• Просмотр основной информации о компании
• История руководителей
• Список учредителей
• Адреса регистрации
• Виды деятельности (ОКВЭД)
• Судебные дела (sudrf.ru)
• Государственные закупки (zakupki.gov.ru)
• Экспорт данных в PDF

<b>Кэширование:</b>
Результаты поиска кэшируются на 1 час для быстрого доступа.

<b>Источники данных:</b>
• DaData API (основная информация)
• sudrf.ru (судебные дела)
• zakupki.gov.ru (госзакупки)
"""
