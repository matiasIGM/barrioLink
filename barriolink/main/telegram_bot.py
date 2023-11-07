import logging 
from telegram import Bot 
 
TELEGRAM_BOT_TOKEN = '6337198782:AAEFHDdar4w6YbU3FWoAtYUnbUlPATpbfuA' 
 
bot = Bot(token=TELEGRAM_BOT_TOKEN) 
 
def enviar_mensaje_telegram(titulo, contenido, usuarios_ids): 
    try: 
        mensaje = f'Nueva publicaci�n: {titulo}\\n\\n{contenido}' 
        for usuario_id in usuarios_ids: 
            bot.send_message(chat_id=usuario_id, text=mensaje) 
    except Exception as e: 
        logging.error(f'Error al enviar mensaje de Telegram: {str(e)}') 
