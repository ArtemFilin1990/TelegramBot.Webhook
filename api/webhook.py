"""
Vercel webhook endpoint for Telegram bot.

This serverless function handles incoming Telegram updates.
"""
import json
import logging
import sys
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

# Add parent directory to path
sys.path.insert(0, '..')

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters
)

from config import config
from bot.handlers.main import start_command, help_command, main_menu_callback, help_callback
from bot.handlers.search import (
    search_inn_callback,
    search_ogrn_callback,
    handle_inn_input,
    handle_ogrn_input,
    cancel_handler,
    AWAITING_INN,
    AWAITING_OGRN
)
from bot.handlers.company import (
    show_company_callback,
    show_finances_callback,
    show_requisites_callback,
    show_address_callback,
    show_directors_callback,
    show_founders_callback,
    show_addresses_history_callback,
    show_okved_callback,
    show_history_menu_callback,
    show_export_menu_callback
)
from bot.handlers.export import export_screen_callback, export_full_callback
from bot.handlers.external import (
    show_court_cases_callback,
    show_procurement_callback,
    handle_pagination
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, config.LOG_LEVEL)
)
logger = logging.getLogger(__name__)

# Global application instance
application = None


def get_application():
    """Get or create application instance."""
    global application
    
    if application is None:
        # Validate config
        config.validate()
        
        # Create application
        application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
        
        # Add conversation handler for search
        conv_handler = ConversationHandler(
            entry_points=[
                CallbackQueryHandler(search_inn_callback, pattern='^search_inn$'),
                CallbackQueryHandler(search_ogrn_callback, pattern='^search_ogrn$'),
            ],
            states={
                AWAITING_INN: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_inn_input)],
                AWAITING_OGRN: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ogrn_input)],
            },
            fallbacks=[CommandHandler('cancel', cancel_handler)],
        )
        
        application.add_handler(conv_handler)
        
        # Add command handlers
        application.add_handler(CommandHandler('start', start_command))
        application.add_handler(CommandHandler('help', help_command))
        
        # Add callback query handlers
        application.add_handler(CallbackQueryHandler(main_menu_callback, pattern='^main_menu$'))
        application.add_handler(CallbackQueryHandler(help_callback, pattern='^help$'))
        
        # Company screens
        application.add_handler(CallbackQueryHandler(show_company_callback, pattern='^company:'))
        application.add_handler(CallbackQueryHandler(show_company_callback, pattern='^brief:'))
        application.add_handler(CallbackQueryHandler(show_finances_callback, pattern='^finances:'))
        application.add_handler(CallbackQueryHandler(show_requisites_callback, pattern='^requisites:'))
        application.add_handler(CallbackQueryHandler(show_address_callback, pattern='^address:'))
        application.add_handler(CallbackQueryHandler(show_history_menu_callback, pattern='^history:'))
        
        # History sub-screens
        application.add_handler(CallbackQueryHandler(show_directors_callback, pattern='^directors:'))
        application.add_handler(CallbackQueryHandler(show_founders_callback, pattern='^founders:'))
        application.add_handler(CallbackQueryHandler(show_addresses_history_callback, pattern='^addresses_history:'))
        application.add_handler(CallbackQueryHandler(show_okved_callback, pattern='^okved:'))
        
        # External modules
        application.add_handler(CallbackQueryHandler(show_court_cases_callback, pattern='^court:'))
        application.add_handler(CallbackQueryHandler(show_procurement_callback, pattern='^procurement:'))
        
        # Pagination
        application.add_handler(CallbackQueryHandler(handle_pagination, pattern='^(court|procurement):(next|prev):'))
        
        # Export
        application.add_handler(CallbackQueryHandler(show_export_menu_callback, pattern='^export_menu:'))
        application.add_handler(CallbackQueryHandler(export_screen_callback, pattern='^export_screen:'))
        application.add_handler(CallbackQueryHandler(export_full_callback, pattern='^export_full:'))
        
        logger.info("Application initialized")
    
    return application


class handler(BaseHTTPRequestHandler):
    """Vercel serverless function handler."""
    
    def do_POST(self):
        """Handle POST request from Telegram."""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            
            logger.info(f"Received webhook: {body[:200]}")
            
            # Parse update
            update_data = json.loads(body)
            update = Update.de_json(update_data, get_application().bot)
            
            # Process update
            import asyncio
            asyncio.run(get_application().process_update(update))
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'ok': True}).encode())
            
        except Exception as e:
            logger.error(f"Error processing webhook: {e}", exc_info=True)
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'ok': False, 'error': str(e)}).encode())
    
    def do_GET(self):
        """Handle GET request (health check)."""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            'status': 'ok',
            'message': 'Telegram Bot Webhook is running'
        }).encode())
