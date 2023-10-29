from telegram import Update
from telegram.ext import Dispatcher, CommandHandler, CallbackContext
from django_telegrambot.apps import DjangoTelegramBot
from django.http import JsonResponse
#from django.views.decorators.csrf import csrf_exempt
from django.views import View
import json

# manejo de vistas y lógica del bot de Telegram 

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hola!')

def setup_dispatcher(dp: Dispatcher):
    dp.add_handler(CommandHandler('start', start))

# manejo ed solicitudes del webhook
class TelegramWebhook(View):
    def post(self, request, *args, **kwargs):
        json_str = request.body.decode('UTF-8')
        update = json.loads(json_str)
        return JsonResponse({'status': 'ok'})