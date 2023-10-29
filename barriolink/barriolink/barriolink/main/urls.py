from django.urls import path
from . import views
from django.urls import path
from . import telegram_views  # telegram
from telegram.ext import Dispatcher
from django_telegrambot.apps import DjangoTelegramBot

urlpatterns = [
      path('', views.home, name='home'),
      path('home', views.home, name='home'),
      path('sign-up', views.sign_up, name='sign_up'),
      path('create-post', views.create_post, name='create_post'),
]

# función del bot - se encarga de agregar los manejadores de comandos a Dispatcher
dispatcher = Dispatcher(DjangoTelegramBot.get_bot().telegram, None, workers=0)
telegram_views.setup_dispatcher(dispatcher)


