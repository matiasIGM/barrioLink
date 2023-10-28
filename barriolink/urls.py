"""
URL configuration for barriolink project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.urls import path
from . import telegram_views  # Importa vistas de telegram
from telegram.ext import Dispatcher
from django_telegrambot.apps import DjangoTelegramBot
from django.urls import path
from .views import TelegramWebhook

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', include('django.contrib.auth.urls')),
    path('telegram_webhook/', TelegramWebhook.as_view(), name='telegram_webhook')
]


# manejadores de comandos a Dispatcher
dispatcher = Dispatcher(DjangoTelegramBot.get_bot().telegram, None, workers=0)
telegram_views.setup_dispatcher(dispatcher)





