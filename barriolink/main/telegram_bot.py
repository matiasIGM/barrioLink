import logging 
from telegram import Bot 
 
TELEGRAM_BOT_TOKEN = '6337198782:AAEFHDdar4w6YbU3FWoAtYUnbUlPATpbfuA' 

# Lista de IDs de chat de los usuarios a los que deseas enviar mensajes
USUARIOS_IDS = [6427719132]

bot = Bot(token=TELEGRAM_BOT_TOKEN) 
 
def enviar_mensaje_telegram(titulo, contenido):
    try:
        mensaje = f'Nueva publicación: {titulo}\n\n{contenido}'
        
        # Envía el mensaje a los usuarios
        for usuario_id in USUARIOS_IDS:
            bot.send_message(chat_id=usuario_id, text=mensaje)

    except Exception as e:
        logging.error(f'Error al enviar mensaje de Telegram: {str(e)}')