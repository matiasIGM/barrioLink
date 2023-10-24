import telegram

# almacena funciones de utilidad y lógica específica del bot 
def enviar_mensaje(usuario_id, mensaje):
    bot_token = '6337198782:AAEFHDdar4w6YbU3FWoAtYUnbUlPATpbfuA'
    bot = telegram.Bot(token=bot_token)
    bot.send_message(chat_id=usuario_id, text=mensaje)


